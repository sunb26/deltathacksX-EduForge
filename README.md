# EduForge: One Stop Study Shop :punch:

## Inspiration
The genesis of EduForge was rooted in a common lament among students: the lack of sufficient practice material for midterms and exams. Professors, often constrained by time, found it challenging to create additional practice questions. This gap in educational resources sparked the idea for EduForge, aiming to empower students with adequate preparation tools.

## What it does

EduForge creates the ultimate study experience. It ingeniously generates custom flashcards and practice midterms based on user-uploaded course notes. Additionally, it tracks study hours over time, enabling users to measure and optimize their productivity.

## How we built it

Our approach to building EduForge was multifaceted:

* We harnessed the power of Cohere's Large Language Model for chat generation.
* We integrated RAG (Retrieval-Augmented Generation) with a Redis Cloud DB instance for dynamic data handling.
* We utilized PostgreSQL Neon DB as our relational database for structured data storage.
* The entire web application was built using Python and Streamlit, offering a responsive and interactive user interface.

## Challenges we ran into
Our journey with EduForge wasn't without its hurdles. The most prominent challenge was the scarcity of human resources, which often made progress slower than desired. Streamlit, while efficient, posed limitations in customization. Additionally, getting the most out of Cohere's LLM required intricate prompt engineering for accuracy in content generation.

## Accomplishments that we're proud of

Despite these challenges, we are immensely proud of what we've achieved with EduForge. The platform is not only functional but also adheres to clean coding practices, emphasizing modules for reusability. We successfully integrated cutting-edge technology, marking a significant milestone in our full-stack development journey.

## What we learned

The development process was a profound learning experience. We discovered the effectiveness of few-pass and few-shot prompting in maintaining deterministic responses. The importance of document chunking was crucial to manage token limits. Surprisingly, the project demanded both NoSQL and SQL databases, a unique combination for our use case. Moreover, this was our maiden venture with Streamlit, adding a new skill to our repertoire.

## What's next for EduForge: One Stop Study Shop

Looking ahead, we have exciting plans for EduForge:

* Implementing a chat UI to enhance user interaction with the bot.
* Transitioning from Streamlit to a more scalable platform due to its performance bottlenecks.
* Enhancing the user interface to make it more visually appealing.
* Refining our prompting techniques for better output from the LLM.
* Exploring vector search for future chat UI implementations in RAG.

EduForge is poised to redefine the study experience, and we are just getting started on this journey of educational innovation.
