import openai
import json

# Set your OpenAI API Key securely
openai.api_key = 'your-openai-api-key'

# Function to generate the comic script using GPT-4
def generate_comic_script(user_input):
    messages = [
        {"role": "system", "content": "You are a creative AI that generates comic scripts."},
        {"role": "user", "content": f"Create a comic script based on this idea: {user_input}. Break it into panels with descriptions and dialogues."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    
    script = response['choices'][0]['message']['content'].strip()
    return script

# Function to generate comic panel images using OpenAI's DALL·E API
def generate_comic_image(panel_description):
    response = openai.Image.create(
        prompt=panel_description,
        n=1,
        size="512x512"
    )
    
    return response['data'][0]['url']  # Extract the generated image URL

# Function to create a structured comic
def create_comic(user_input):
    comic_script = generate_comic_script(user_input)
    
    print("Generated Comic Script:\n")
    print(comic_script)
    
    # Splitting panels using numbered formatting (e.g., "Panel 1:", "Panel 2:")
    panels = [p.strip() for p in comic_script.split("Panel ") if p]
    
    comic_data = []
    
    for panel in panels:
        panel_number = panel.split(":")[0]
        panel_description = ":".join(panel.split(":")[1:]).strip()
        
        print(f"\nGenerating image for {panel_number}...")
        image_url = generate_comic_image(panel_description)
        
        comic_data.append({
            "panel": panel_number,
            "text": panel_description,
            "image_url": image_url
        })
    
    return comic_data

# Example: Create a comic based on a user input
user_input = "A time traveler meets their past self in a cyberpunk city."
comic = create_comic(user_input)

# Display the output
print("\nFinal Comic:")
for panel in comic:
    print(f"\n{panel['panel']}: {panel['text']}")
    print(f"Image: {panel['image_url']}")
