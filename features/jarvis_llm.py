'''
from transformers import pipeline 
from features.jarvis_voice import JarvisVoice
import utils
import wikipedia
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Jarvis_LLM :
      
      def __init__(self,model_name = "google/flan-t5-base"):
        self.data = utils.get_file()
        self.generate = pipeline("text2text-generation", model=model_name)  

      def ask(self,prompt : str) -> str:
        response = self.generate(prompt,max_new_tokens=100, do_sample=True)
        return response[0]['generated_text']
      

      def wikipedia_data():
        pass
      def data_clean(self,Rawdata):
          for keyword in self.data["search"]["web"]:
              if keyword in Rawdata:
                parts = Rawdata.split(keyword,1)
                if len(parts) > 1:
                    cleanedData = parts[1].strip()
                    # ✅ directly call internet_qa_with_image here
                    return self.getClearedData(cleanedData)

      def getClearedData(self,data):
          prompt = f"Answer the following question accurately and factually in one sentence:\nQuestion: {data}\nAnswer:"
          reply = self.ask(prompt)
          print("Jarvis:", reply)
          print(reply)
      
'''
import sys, os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

class Jarvis_LLM:
    def __init__(self, data):
        # Load data for keywords
        self.data = data

        # Load environment variables
        load_dotenv()
        self.hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if not self.hf_token:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in .env")

        # Initialize HuggingFaceEndpoint
        try:
            self.llm = HuggingFaceEndpoint(
                repo_id="bigscience/bloom-560m",
                temperature=0.5,
                max_new_tokens=100,
                huggingfacehub_api_token=self.hf_token
            )
            print("HuggingFaceEndpoint initialized successfully.")
        except Exception as e:
            print("Error initializing HuggingFaceEndpoint:")
            import traceback
            traceback.print_exc()
            raise e

    def data_clean(self, raw_data):
        """Check for keywords in 'search->web' and clean the query for LLM"""
        try:
            for keyword in self.data.get("search", {}).get("web", []):
                if keyword.lower() in raw_data.lower():
                    parts = raw_data.split(keyword, 1)
                    if len(parts) > 1:
                        cleaned_data = parts[1].strip()
                        return self.get_cleared_data(cleaned_data)
        except Exception as e:
            print("Error in data_clean():")
            import traceback
            traceback.print_exc()

    def get_cleared_data(self, data):
        """Invoke HuggingFaceEndpoint with cleaned query"""
        try:
            response = self.llm.invoke(data)
            print("LLM Response:", response)
            print(response)
            return response
        except Exception as e:
            print("Error in get_cleared_data():")
            import traceback
            traceback.print_exc()
