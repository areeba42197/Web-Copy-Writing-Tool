import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv  # Import `load_dotenv` to load environment variables
import os


load_dotenv()  

API_KEY = os.getenv("API_KEY")  
genai.configure(api_key=API_KEY)


st.set_page_config(
    page_title="AI-Powered Web Content Generator",  # Title for the browser tab
    page_icon="🌐",  
)


def generate_prompt(page_type, website_description, word_count):
    """
    Generate a professional, plagiarism free, and SEO-optimized prompt based on page type, website description, and word count.

    Parameters:
        page_type (str): Type of the page (e.g., Home, About Us, Contact Us, etc.)
        website_description (str): Brief description of the website.
        word_count (int): The word count desired for the output.

    Returns:
        str: The generated prompt for the model.
    """
    page_prompts = {
        "Home ": f"Craft an engaging homepage copy (around {word_count} words) for a website that offers {website_description}. The content should immediately communicate the brand's value proposition and highlight its core identity, especially focusing on eco-friendly and sustainable aspects. Start with a compelling, attention-grabbing introduction, followed by concise, easy-to-read paragraphs. Share a brief and impactful brand story that resonates with the audience's needs and challenges. Emphasize the business's dedication to sustainability and environmental responsibility. Incorporate social proof, such as testimonials or achievements, to build credibility. End with a clear, action-oriented call-to-action (CTA) that encourages visitors to take the next step, whether it’s subscribing, purchasing, or exploring further. Ensure the tone is inviting, concise, and aligned with the brand's values. Use short paragraphs of not more than 3 lines , proper spacing, and an aesthetically pleasing format for easy readability.",

        "About Us": f"Write an About Us page copy (around {word_count} words) for a website. The website offers: {website_description}. Emphasize the business's mission, values, history, and vision for the future. Include information on why the business is credible (such as achievements, collaborations, or industry recognition). Address potential visitor questions like: 'Is this brand legit?' and 'Do I resonate with this brand’s values and mission?' Present the business’s story in a way that establishes trust and invites visitors to connect. Conclude with a call to action (CTA), encouraging visitors to take the next step (e.g., explore services, contact the business, or follow on social media).Use simple words.Donot use large paragraphs , proper spacing, and an aesthetically pleasing format for easy readability.",

        "Contact Us": f"Write a Contact Us page copy (around {word_count} words) for a website. The website provides: {website_description}. The copy should encourage users to get in touch by making it easy for them to reach out. Highlight the various contact methods (e.g., contact form, email, phone number, live chat) and customer support options. Include a brief invitation to contact, provide multiple avenues for getting in touch, and offer social proof (e.g., logos, testimonials). Conclude with a call-to-action that makes reaching out easy and compelling.Use simple words.Donot use large paragraphs ,use  proper spacing, and an aesthetically pleasing format for easy readability.",

        "Products": f"Write a Products page copy (around {word_count} words) for a website. The website offers: {website_description}. Highlight the unique selling points of the products, any customization options, and the benefits for customers. Create a compelling product name. Provide essential technical details and specifications like material, dimensions, and weight. Include any relevant information customers might actively look for. Use clear and actionable copy for the ‘Add to Cart’ button (e.g., ‘Add to Cart’ or ‘Buy Now’). Include customer reviews and a strong call-to-action to purchase.Donot use large paragraphs ,use  proper spacing, and an aesthetically pleasing format for easy readability.",

        "Services": f"Write a Services page copy (around {word_count} words) for a website. The website offers: {website_description}. Clearly explain the services offered, highlight what makes them unique, outline the specific benefits for customers, and explain how these services solve key problems or improve the customer's experience. Include a call-to-action (CTA) to encourage readers to contact or engage with the service.Donot use large paragraphs ,use  proper spacing, and an aesthetically pleasing format for easy readability.",

        "Landing": f"Write an engaging landing page copy (around {word_count} words) for a website that provides {website_description}. The copy should focus on persuading visitors to take immediate action while reinforcing the core benefits of the product or service. Start with a bold and attention-grabbing headline that clearly communicates what the business offers. Follow with a compelling subheading that explains how the product or service solves the visitors' pain points. Use bullet points to succinctly outline key features and advantages, emphasizing how the brand stands out in terms of quality, sustainability, and eco-friendliness. Conclude with a clear, action-oriented call-to-action (CTA) that encourages visitors to engage with the business.Donot use large paragraphs ,use  proper spacing, and an aesthetically pleasing format for easy readability.",

        "FAQs": f"Write a Frequently Asked Questions (FAQ) page copy (around {word_count} words) for a website that offers {website_description}. The page should include a clear and concise list of common questions customers might ask, along with detailed and helpful answers. Organize the FAQ into sections, ensuring each answer is informative and addresses the user's needs.Each section should be in different paragrapg and all questions shoould first include question as heading and its answer in next line. Everything question and its answer should in seperate line . Prioritize clarity, simplicity, and usefulness in every response to improve the user experience.Donot use large paragraphs ,use  proper spacing, and an aesthetically pleasing format for easy readability."
    }

    return page_prompts.get(page_type, "Invalid page type. Please select from: Home, About, Landing Page, Contact, Products, Services, FAQs.")

def generate_copy_with_gemini(model, prompt):
    """
    Generate web copy using the Gemini API.

    Parameters:
        model (str): The name of the Gemini model to use.
        prompt (str): The prompt for generating web copy.

    Returns:
        str: The generated web copy.
    """
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)
    
    generated_text = response.text.strip()
    
    word_limit = int(prompt.split('around ')[1].split(' words')[0])
    generated_words = generated_text.split()
    if len(generated_words) > word_limit:
        generated_text = ' '.join(generated_words[:word_limit])  # Trim to the word limit
    
    return generated_text  # Return the generated web copy

def main():
    """
    Main function to render the Streamlit UI and generate web content.
    """
    st.title("AI-Powered Web Content Generator")
    st.markdown("<h2 style='font-size: 20px;'>Generate professional and SEO-optimized copywriting content for your website that is 100% plagiarism free .</h2>", unsafe_allow_html=True)


    # Input fields for page type, website description, and word count
    page_type = st.selectbox(
        "Select the type of web page:",
        ["Home", "About Us", "Contact Us", "Products", "Services", "Landing", "FAQs"]
    )

    website_description = st.text_area(
        "Enter a brief description of your website:",
        placeholder="e.g., A sustainable online store specializing in eco-friendly fashion. Describe what your website is about (e.g., the products you sell, the services you offer, or your mission)."
    )

    word_count = st.number_input(
        "Enter the desired word count:",
        min_value=50,
        max_value=2000,
        value=300
    )


    st.markdown("""
    <style>
        .stButton > button {
            background-color: #4CAF50;  /* Green background color */
            color: white;  /* White text */
            font-size: 18px;  /* Larger font size */
            padding: 10px 20px;  /* Padding to make the button larger */
            border-radius: 5px;  /* Rounded corners */
            width: 200px;  /* Adjust width */
            display: block;
            margin: 0 auto;  /* Center align */
        }
        .stButton > button:hover {
           background-color: white;  /* White background on hover */
            color: black;  /* Black text on hover */
        }
    </style>
""", unsafe_allow_html=True)

    # Generate content button
    if st.button("Generate Web Copy"):
        if not website_description.strip():
            st.error("Please provide a description of your website.")
        else:
            with st.spinner("Generating content..."):
                prompt = generate_prompt(page_type, website_description, word_count)

                if "Invalid" in prompt:
                    st.error(prompt)
                else:
                    # Provide the model as the first argument to the function
                    model_name = "gemini-1.5-flash"  # Replace with your model name (e.g., "gemini-v1")
                    web_copy = generate_copy_with_gemini(model_name, prompt)
                    st.success(f"Generated {page_type} Page Content")
                    st.text_area("Generated Web Copy:", value=web_copy, height=300)

if __name__ == "__main__":
    main()
