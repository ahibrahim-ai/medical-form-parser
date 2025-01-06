# medical-form-parser

### **Project Overview: Clinic Form Table Converter with Gemini LLM**

This project is designed to automate the process of extracting structured information from medical clinic registration forms stored as images in Google Cloud Storage (GCS). By leveraging Google Cloud's Vertex AI and the Gemini Large Language Model (LLM), the script processes image-based forms, extracts key patient details, and outputs structured data in JSON format.

---

### **Key Features**

1. **Automated Image Processing**
   - Supports images in `.jpg`, `.jpeg`, and `.png` formats.
   - Lists and processes all images in a specified GCS bucket.

2. **AI-Driven Data Extraction**
   - Uses the Gemini LLM to extract key fields such as:
     - **Title**
     - **First Name**
     - **Last Name**
     - **Contact Number**
     - **Date of Birth (DOB)**
     - **Address**
     - **Postcode**

3. **Output as Structured JSON**
   - Extracted information is saved in a well-formatted JSON file.
   - Handles multiple images and aggregates the results into a single output file.

4. **Error Handling**
   - Robust error handling ensures the script continues processing even if some images fail.
   - Logs errors for images that cannot be processed.

---

### **Technical Details**

- **Language**: Python 3.8+
- **Frameworks & Libraries**:
  - `google.cloud.storage` for interacting with GCS.
  - `vertexai` for initialising and using the Gemini LLM.
  - `json` for handling structured data output.
  - `os` for file path operations.

- **Deployment**:
  - Designed for local execution or deployment on a cloud environment (e.g., Google Cloud Run).
  - Requires appropriate IAM permissions to access GCS and Vertex AI.

---

### **Usage**

1. **Setup**:
   - Ensure you have a Google Cloud project with Vertex AI and Cloud Storage APIs enabled.
   - Set up authentication by downloading the service account key JSON file and setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

2. **Execution**:
   - Replace `PROJECT_ID` and `bucket_name` in the script with your Google Cloud project ID and GCS bucket name.
   - Run the script using Python:
     ```bash
     python app.py
     ```

3. **Output**:
   - The script generates an `output.json` file containing the extracted information from all processed images.

---

### **Future Enhancements**

- **Field Validation**: Improve the accuracy of extracted data by adding validation rules for specific fields (e.g., phone number format, date validation).
- **Additional Output Formats**: Support exporting data to CSV or Excel in addition to JSON.
- **Multi-language Support**: Enable processing of forms in multiple languages.
- **Web Interface**: Add a simple web interface for uploading forms and downloading the results directly.

---

### **Conclusion**

This project streamlines the workflow for medical clinics by automating the tedious task of manually extracting patient information from image-based registration forms. With the power of Google Cloud and Gemini LLM, the solution provides a scalable and efficient approach to data extraction, ensuring accuracy and saving valuable time.

