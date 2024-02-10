# chat-web
Making chatbots better.



# Serve models locally
We can serve models locally using Ollama. 
1. Download the Ollama of your OS. Currently, it is not available for Windows. 
https://ollama.com/download
```curl -fsSL https://ollama.com/install.sh | sh```

2. Check the documentation below to find out how to download the model that is required. 
https://github.com/ollama/ollama
Example, running the command below will downloadn the llama2 model the first time and host it in the locahost. 
```ollama run mistral```
3. The models are hosted in the port mentioned below: 
 http://localhost:11434/api/generate
 Enjoy!


