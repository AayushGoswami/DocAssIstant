import os
import logging
from typing import Optional, List
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
from groq import Groq

# Load environment variables
load_dotenv()
class AIProcessor:
    
    def __init__(self):
        
        # Use provided API key or try to get from environment
        api_key = os.environ.get('GROQ_API_KEY')
        
        if not api_key:
            raise ValueError("No Groq API key provided. Set GROQ_API_KEY environment variable.")
        
        # Initialize the Groq client
        self.client = Groq(api_key=api_key)

                # Initialize TFLite model for X-ray analysis
        self.xray_interpreter = tf.lite.Interpreter(model_path='utils/models/chest_xray_model_quantized.tflite')
        self.xray_interpreter.allocate_tensors()
        
        # Get input and output details for X-ray model
        self.xray_input_details = self.xray_interpreter.get_input_details()
        self.xray_output_details = self.xray_interpreter.get_output_details()

    


    ### MEDICAL REPORT ANALYZER PROCESSES ###



    def summarize_medical_document(
        self, 
        text: str,
    ) -> str:

        try:
            # Validate input
            if not text or len(text.strip()) < 10:
                return "Insufficient text for meaningful analysis."
            
            # Construct prompt
            prompt = f"""Analyze and summarize the following medical document.
            Maintain a professional tone and focus on key medical insights. 
            Provide a clear, concise summary highlighting key medical insights, 
            important parameters, and any potential areas of concern:

            {text}
                    """
            
            # Generate summary
            chat_completions = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": "Summary: "
                        }
                ],
                model="llama-3.2-11b-vision-preview",
                max_tokens=1024,
                temperature=0.7,
            )
            # print(chat_completions.choices[0].message.content.strip())
            # Extract and return the summary text
            return chat_completions.choices[0].message.content.strip()
        
        except Exception as e:
            logging.error(f"Error in AI summarization: {e}")
            return f"Error in AI analysis: {str(e)}"
    
    def analyze_medical_parameters(
        self, 
        text: str, 
        parameters: Optional[List[str]] = None
    ) -> dict:

        try:
            # Default parameters if none provided
            if not parameters:
                parameters = [
                    # Basic blood panel
                    'hemoglobin', 'white blood cell count', 'platelets', 
                    'red blood cell count', 'mean corpuscular volume', 'hematocrit',
                    
                    # Blood chemistry
                    'blood glucose', 'HbA1c', 'creatinine', 'urea', 
                    'sodium', 'potassium', 'chloride', 'calcium', 
                    'magnesium', 'phosphate', 'bilirubin', 'alkaline phosphatase',
                    'alanine transaminase (ALT)', 'aspartate transaminase (AST)', 
                    'lactate dehydrogenase (LDH)', 'albumin', 'total protein',
                    
                    # Lipid panel
                    'total cholesterol', 'LDL cholesterol', 'HDL cholesterol', 
                    'triglycerides', 'cholesterol/HDL ratio',
                    
                    # Hormonal markers
                    'thyroid stimulating hormone (TSH)', 'free T3', 'free T4', 
                    'cortisol', 'estrogen', 'progesterone', 'testosterone',
                    'insulin', 'parathyroid hormone (PTH)', 'prolactin',
                    
                    # Inflammatory markers
                    'C-reactive protein (CRP)', 'erythrocyte sedimentation rate (ESR)', 
                    'interleukin-6 (IL-6)', 'tumor necrosis factor alpha (TNF-α)',
                    
                    # Cancer markers
                    'prostate-specific antigen (PSA)', 'CA-125', 'CA 19-9', 
                    'alpha-fetoprotein (AFP)', 'CEA', 'beta-hCG',
                    
                    # Nutritional markers
                    'iron', 'ferritin', 'transferrin saturation', 
                    'vitamin D', 'vitamin B12', 'folate',
                    
                    # Coagulation profile
                    'prothrombin time (PT)', 'international normalized ratio (INR)', 
                    'activated partial thromboplastin time (aPTT)', 'fibrinogen',
                    
                    # Respiratory and arterial blood gas
                    'oxygen saturation (SpO2)', 'partial pressure of oxygen (PaO2)', 
                    'partial pressure of carbon dioxide (PaCO2)', 'pH', 
                    'bicarbonate (HCO3)', 'base excess',
                    
                    # Miscellaneous parameters
                    'body mass index (BMI)', 'blood pressure', 'heart rate', 
                    'spirometry results (FEV1, FVC)', 'uric acid', 'eGFR',
                    'microalbumin', 'urinary protein',
                    
                    # Imaging-related findings
                    'MRI observations', 'CT scan findings', 'X-ray findings', 
                    'ultrasound measurements', 'echocardiogram results',
                    
                    # Genetic and molecular markers
                    'BRCA1/BRCA2 mutations', 'HLA typing', 'karyotype analysis',
                    'genomic variants'
                ]
            
            # Construct prompt
            prompt = f"""From the following medical document, extract the values 
            for these specific parameters: {', '.join(parameters)}

            Document:
            {text}

            Provide the output in a clear JSON-like format with parameter names as keys 
            and their values. If a parameter is not found, use null."""
            
            # Generate response
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",  # Using the smaller 8b model for this task
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300
            )
            # print(response.choices[0].message.content.strip())
            # Extract and return the parameter analysis
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logging.error(f"Error in parameter extraction: {e}")
            return {"error": str(e)}

    @staticmethod
    def validate_medical_document(text: str) -> bool:

        # Basic validation of whether the text appears to be a medical document.
        
        # Args:
        #     text (str): Text to validate
        
        # Returns:
        #     bool: Whether the text seems to be a medical document
        
        medical_keywords = [
            'patient', 'report', 'blood', 'test', 'result', 
            'medical', 'diagnosis', 'laboratory', 'clinic'
        ]
        
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Check if sufficient medical keywords are present
        keyword_count = sum(1 for keyword in medical_keywords if keyword in text_lower)
        
        return keyword_count >= 3



### COMMON IMAGE PREPROCESSOR FUNCTION ###


    def preprocess_image(self, img_path):
        img = image.load_img(img_path, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0
        return img_array



### X-RAY IMAGE ANALYZER PROCESSES ###



    def analyze_x_ray_image(self, img_path: str) -> str:

        try:
            # Preprocess the image
            img_array = self.preprocess_image(img_path)

            # Set the input tensor
            self.xray_interpreter.set_tensor(self.xray_input_details[0]['index'], img_array)
            
            # Run inference
            self.xray_interpreter.invoke()

            # Get the prediction results
            prediction = self.xray_interpreter.get_tensor(self.xray_output_details[0]['index'])
            # prediction = self.xray_interpreter.get_tensor(self.xray_output_details[0]['index'])
            print(prediction)  # Keep your debug print
            
            # Make a prediction
            # prediction = self.xray_model.predict(img_array)
            # print(prediction)
            
            # Get the class label
            if prediction[0] < 0.5:
                return "The X-ray image appears to be Normal."
            else:
                return "The X-ray image shows signs of Pneumonia."
        
        except Exception as e:
            logging.error(f"Error in AI analysis: {e}")
            return f"Error in AI analysis: {str(e)}"


    def summarize_x_ray(self, text: str,) -> str:

        try:
            # Construct prompt
            prompt = f"""Analyze and summarize the following X-Ray report in breif in a Professional tone.
            
            {text}
                    """
            
            # Generate summary
            chat_completions = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": "Summary: "
                        }
                ],
                model="llama-3.2-11b-vision-preview",
                max_tokens=1024,
                temperature=0.7,
            )
            # Extract and return the summary text
            return chat_completions.choices[0].message.content.strip()
        
        except Exception as e:
            logging.error(f"Error in AI summarization: {e}")
            return f"Error in AI analysis: {str(e)}"



### ECG IMAGE ANALYZER PROCESSES ###


    # Load TFLite model
    ecg_interpreter = tf.lite.Interpreter(model_path='utils/models/ecg_model_quantized.tflite')
    ecg_interpreter.allocate_tensors()
    
    # Get input and output tensors
    input_details = ecg_interpreter.get_input_details()
    output_details = ecg_interpreter.get_output_details()
    
    class_labels = [
        "ECG of Myocardial Infarction Patient",
        "ECG of Patient with Abnormal Heartbeat",
        "ECG of Patient with History of Myocardial Infarction",
        "Normal ECG"
    ]


    def classify_ecg(self, img_path):
        """
        Classify the input ECG image.
        Args:
            img_path (str): Path to the ECG image.
        Returns:
            str: Predicted class label.
        """
        img_array = self.preprocess_image(img_path)
            # Set input tensor
        self.ecg_interpreter.set_tensor(self.input_details[0]['index'], img_array)
        
        # Run inference
        self.ecg_interpreter.invoke()
        
        # Get prediction results
        predictions = self.ecg_interpreter.get_tensor(self.output_details[0]['index'])
        
        # Get predicted class
        predicted_class = np.argmax(predictions, axis=1)[0]
        print(predictions)  # Keep your debug print
        return self.class_labels[predicted_class]


    def summarize_ecg(self, text: str) -> str:
        """
        Summarize the input ECG report.
        Args:
            text (str): ECG report text.
        Returns:
        str: Summarized ECG report.
        """

        try:
            # Construct prompt
            prompt = f"""Analyze and summarize the following ECG Graph Report in brief in a Profesional tone.
            
            {text}
                    """
            
            # Generate summary
            chat_completions = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": "Summary: "
                        }
                ],
                model="llama-3.2-11b-vision-preview",
                max_tokens=1024,
                temperature=0.7,
            )
            # Extract and return the summary text
            return chat_completions.choices[0].message.content.strip()
        
        except Exception as e:
            logging.error(f"Error in AI summarization: {e}")
            return f"Error in AI analysis: {str(e)}"
