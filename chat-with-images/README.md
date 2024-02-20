
## Introduction 
In the rapidly advancing field of artificial intelligence, the integration of symbolic AI systems like Operational Decision Management (ODM) with cutting-edge computer vision models such as Llava presents a groundbreaking approach. ODM, a platform known for its robust rule-based decision-making capabilities, excels in structuring complex logic and business rules into coherent, manageable systems. This enables precise, consistent decision-making processes across various business applications, from finance to healthcare.

Conversely, Llava, a state-of-the-art computer vision model, epitomizes the pinnacle of deep learning's ability to interpret and analyze visual data. By transforming raw images and video into actionable insights, Llava extends the boundaries of how machines understand and interact with the visual world around them.

The fusion of ODM's logical rigor with Llava's perceptive prowess creates a symbiotic AI system that leverages the strengths of both symbolic reasoning and deep learning. This article aims to showcase, through practical code demonstrations, the synergistic benefits of combining ODM's rule-based intelligence with Llava's visual acuity. By doing so, we can tackle more nuanced and complex problems that were previously beyond the reach of AI systems operating in isolation.

We will delve into specific scenarios where the ODM-Llava integration unlocks new possibilities, from enhancing automated surveillance systems with intelligent decision-making to revolutionizing medical diagnostics with visually informed rule-based analyses. This exploration will not only highlight the individual strengths of ODM and Llava but also illuminate how their combination paves the way for innovative AI applications that are smarter, more efficient, and more aligned with human-like reasoning and perception.


## Architecture
![Console with Business console](images/presentation.png)

In this prototype we use the RAG architecture.
In the context of artificial intelligence, RAG stands for “Retrieval-Augmented Generation”. It is a relatively new technique that improves the quality of generative AI systems by allowing large language models (LLMs) to access additional data resources without needing to be retrained. In other words, RAG optimizes the output of an LLM with targeted information without modifying the underlying model itself. This targeted information can be more up-to-date than the LLM and specific to a particular organization or industry. This means that the generative AI system can provide more contextually appropriate responses to prompts and base them on extremely current data.
By this way, we are able to augment the LLM model with the ODM documentation. 

## Pre-requisites
  * Docker
  * docker-compose
  * Macbook M1 or equivalent. 

## Setup Pre-Requisites


### Install Ollama
[Ollama](https://ollama.ai/) allows you to run open-source large language models, such as Llama 2, locally.

Ollama bundles model weights, configuration, and data into a single package, defined by a Modelfile.

It optimizes setup and configuration details, including GPU usage.

1. [Download and run](https://ollama.ai/download) the app
2. Once Ollma is up and running, you should download a model. For this sample we will used Mistra model.
For a complete list of supported models and model variants, see the [Ollama model library](http://ollama.ai/library).
3. From command line, fetch the mistra model.
   
```shell
ollama pull llava:v1.6
```

When the app is running, all models are automatically served on [localhost:11434](http://localhost:11434)


### Run the images application

1. Open a new terminal
2. Build the docker demonstration 
```shell
docker-compose build
```
Once the build is finished.

3. Run the demonstration
```shell
docker-compose up
```
This will run the ODM for Developpers docker images in conjonction with the sample web application.

4. Wait a couple of minutes until you see this message  ```Running on local URL:  http://0.0.0.0:7860```
5. Then open a browser to this url : http://localhost:7860

and select , upload and take a photo then click the ```Analyse Image``` button.

You can browse to Rules that is applyied in the sample by :
  * 1. Open Decision Center at this location : http://localhost:9060/decisioncenter
      * Username : odmAdmin
      * Password : odmAdmin
  * 2. Go to the Library 
      * Click the import button 
      * Select in the data/project.zip
      

![Console with ODM Documentation](images/chatwithodmdoc.gif)


