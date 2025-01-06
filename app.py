import os
import json
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError

# Function to initialize Vertex AI and set up authentication
def initialize_vertex_ai():
    try:
        # Get project ID from environment variable or prompt user
        project_id = os.getenv("PROJECT_ID")
        location = "us-central1"  # Set location (can be parameterized if needed)
        
        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)
        
        # Initialize the Gemini LLM model
        model = GenerativeModel("gemini-2.0-flash-exp", generation_config={"response_mime_type": "application/json"})
        return model
    except DefaultCredentialsError as e:
        print("Error: Google Cloud credentials not found.")
        print("Set the GOOGLE_APPLICATION_CREDENTIALS environment variable or authenticate using `gcloud auth application-default login`.")
        raise e

def list_gcs_images(bucket_name, prefix=""):
    """List all image files in a GCS bucket under a specific prefix."""
    try:
        storage_client = storage.Client()
        blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
        
        image_paths = [
            f"gs://{bucket_name}/{blob.name}"
            for blob in blobs
            if blob.name.lower().endswith(('.jpg', '.jpeg', '.png')) and not blob.name.endswith('/')
        ]
        return image_paths
    except Exception as e:
        print(f"Error listing images in bucket {bucket_name}: {e}")
        return []

def process_image_with_gemini_llm(image_path, model):
    """Use Gemini LLM to analyze an image and generate structured content."""
    if not image_path.startswith("gs://"):
        print(f"Invalid image path: {image_path}")
        return None
    
    try:
        response = model.generate_content(
            [
                Part.from_uri(image_path, mime_type="image/jpeg"),
                """
                Extract and structure the following information from the image into a table with these columns:
                First Name, Last Name, Birth Date, Address, ZIP.
                Return the result as structured JSON.
                """
            ]
        )
        raw_text = response.text.strip()

        # Remove backticks if they exist around the response
        if raw_text.startswith("```json\n[\n  {\n    ") and raw_text.endswith("```"):
            raw_text = raw_text[3:-3].strip()

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            print(f"JSON decode error for image {image_path}: {e}")
            print(f"Raw response: {raw_text}")
            return None


    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def process_all_images_in_bucket(bucket_name, output_file="output.json"):
    """Process all images in a GCS bucket and save the results as a JSON file."""
    # Initialize the model
    model = initialize_vertex_ai()
    
    image_paths = list_gcs_images(bucket_name)
    all_results = []

    for image_path in image_paths:
        llm_output = process_image_with_gemini_llm(image_path, model)
        if llm_output:
            all_results.append(llm_output)
    
    if all_results:
        with open(output_file, "w") as f:
            json.dump(all_results, f, indent=4)
        print(f"Results saved to {output_file}")
    else:
        print("No valid data extracted from the images.")

# Usage Example
if __name__ == "__main__":
    bucket_name = os.getenv("BUCKET_NAME")  # Replace with your GCS bucket name or set as an env variable
    try:
        process_all_images_in_bucket(bucket_name)
    except Exception as e:
        print(f"Script failed: {e}")
