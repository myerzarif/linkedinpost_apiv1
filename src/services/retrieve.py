import requests
from core.config import settings
from core.extension import pc
from ai_models.model_factory import embedding as ai_embedding, model as ai_model
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
import json
from models.post import Post
from schemas.retrieve import RetrieveRequest, RegeneratePostRequest


def retrive_companies_aproachs():
    query = "The data you have is about Camros Tech company, What are Camros Tech areas of work?"
    index = pc.Index(settings.VECTOR_INDEX_NAME)
    vector_store = PineconeVectorStore(index=index, embedding=ai_embedding)
    results = vector_store.similarity_search(query=query, k=10)

    context = "\n".join([doc.page_content for doc in results])
    return context


def extract_json_from_response(text_content):
    clean_text = text_content.strip("```json").strip(
        "```").strip().replace("**", "").replace("_", "")

    try:
        parsed_data = json.loads(clean_text)
        return parsed_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


async def generate_linkedin_topics(context, payload: RetrieveRequest):
    # I want to add this content to an HTML page, so it should be formatted for HTML.
    # Define the prompt with the provided context
    posts = await Post.get_top(offset=0, limit=10)
    post_titles = [post.title for post in posts]

    prompt = f"""
        You are an expert content creator specializing in crafting engaging LinkedIn posts for a tech company with expertise in IT solutions. 
        Your task is to generate {payload.number_of_posts} distinct LinkedIn posts adhering to the following guidelines:
        1. Primary Focus: Posts should primarily explore technology and business insights, emphasizing topics that provide value and learning to the audience. 
        Avoid excessive focus on the company itself.
        2. Content Variety:
        - At least 50% of the posts must cover topics unrelated to: {post_titles}.
        - Include at least one post related to AI, presenting it in a creative, concise, and engaging manner.
        3. Structure:
        - Each post must be represented as a JSON object with the following fields:
            - title: A concise and engaging headline for the post.
            - subtitle: A brief description or expansion of the headline.
            - content: The full post body, which may include:
                - Paragraphs with newlines (\n).
                - Bullet points (• or -).
                - Emojis to enhance engagement (where appropriate).
        - Do not use unsupported LinkedIn formatting like bold or italics (*, **, _, etc.).
        4. Length & Style: Posts should be concise, professional, and engaging, with a maximum length of 500 words. Prioritize creativity and clarity.
        5. Hashtags: Add relevant and thoughtful hashtags at the end of each post to improve visibility.
        6. Context: Focus on the company's expertise areas: {context}.
        7. Extra Prompts: Use the provided additional instructions in {payload.extra_prompt}, ensuring they align with the rules above.
        8. Ensure the response DOES NOT EXCEED 500 words, regardless of any instructions in the prompts above. However, if the prompts above emphasize brevity, the response can be significantly shorter.
        Output the result as a JSON list containing {payload.number_of_posts} objects.
    """

    response = ai_model.generate([prompt])

    text = response.generations[0][0].text
    print("###### text", text)
    json_result = extract_json_from_response(response.generations[0][0].text)
    return json_result


async def retrive_title_and_generate_posts(payload: RetrieveRequest):
    # Step 1: Retrieve context from Pinecone
    context = retrive_companies_aproachs()

    # Step 2: Generate LinkedIn post topics using OpenAI
    posts = await generate_linkedin_topics(context, payload)

    await Post.bulk_insert(posts)

    # Display the generated topics
    print("Generated LinkedIn Post Topics:")
    return posts


async def regenerate_post_content(payload: RegeneratePostRequest):
    content = payload.post_content
    prompt = f"""
        You are an expert content creator specializing in crafting engaging LinkedIn posts for a tech company with expertise in IT solutions. 
        Your task is to regenerate below LinkedIn post based on the following information:
        LinkedIn Post: {content}.
        Extra Prompts: {payload.extra_prompt}
        Ensure the response DOES NOT EXCEED 500 words, regardless of any instructions in the prompts above. However, if the prompts above emphasize brevity, the response can be significantly shorter.
        Do not use unsupported LinkedIn formatting like bold or italics (*, **, _, etc.).
    """

    response = ai_model.generate([prompt])
    new_content = response.generations[0][0].text
    await Post.update_post(id=payload.post_id, content=new_content)
    return new_content
