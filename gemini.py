# gemini.py
# AI Interview Assistant — Question Bank + Evaluation Engine
# Supports 20 roles with 50+ questions each.
# Gemini AI is used when available; offline fallback always works.

import os
import re
import json
import random
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# Gemini Client (optional — graceful if unavailable)
# ============================================================

_gemini_client = None

try:
    # pyrefly: ignore [missing-import]
    from google import genai
    _api_key = os.getenv("GEMINI_API_KEY", "")
    if _api_key:
        _gemini_client = genai.Client(api_key=_api_key)
except Exception as _e:
    print(f"[INFO] Gemini unavailable: {_e}. Offline mode active.")


# ============================================================
# QUESTION BANK — 20 Roles × 50+ Questions
# ============================================================

QUESTION_BANK = {

    # ----------------------------------------------------------
    "Software Engineer": [
        # Technical
        "Explain the software development life cycle (SDLC).",
        "What are the differences between stack and heap memory?",
        "Explain object-oriented programming concepts with examples.",
        "What is polymorphism? Give a real-world example.",
        "Explain REST API architecture and its principles.",
        "What are design patterns? Name and explain three commonly used ones.",
        "Explain database indexing and when you would use it.",
        "What is the difference between SQL and NoSQL databases?",
        "Explain multithreading and when it causes problems.",
        "What is version control and why is it important?",
        "Explain Git branching strategies (GitFlow, trunk-based).",
        "What are SOLID principles? Explain each one briefly.",
        "Explain microservices architecture vs monolithic architecture.",
        "What happens step by step when you type a URL in a browser?",
        "Explain caching strategies (LRU, LFU, write-through, write-back).",
        "What is load balancing? Explain different algorithms.",
        "Explain authentication vs authorization.",
        "What is the difference between a compiler and an interpreter?",
        "Explain exception handling best practices.",
        "How do you optimize application performance?",
        "What is Big O notation? Explain O(n log n) with an example.",
        "Explain the CAP theorem in distributed systems.",
        "What is a race condition? How do you prevent it?",
        "Explain dependency injection and inversion of control.",
        "What is a message queue? When would you use Kafka vs RabbitMQ?",
        "Explain the difference between synchronous and asynchronous programming.",
        "What is Docker and how does containerization work?",
        "Explain CI/CD pipelines and their components.",
        "What is technical debt and how do you manage it?",
        "Explain the difference between unit tests, integration tests, and end-to-end tests.",
        # Scenario-based
        "You notice a production API is returning 500 errors. Walk me through your debugging process.",
        "Your team has conflicting opinions on code architecture. How do you resolve it?",
        "You have a task that is taking longer than estimated. What do you do?",
        "Describe a time you refactored a piece of legacy code. What was your approach?",
        "How would you design a URL shortener like bit.ly from scratch?",
        "How would you design a notification system that supports email, SMS, and push?",
        "A feature you deployed caused a regression. What steps do you take?",
        "How would you prioritize bug fixes vs new features?",
        # HR
        "Tell me about yourself and your background in software engineering.",
        "Why do you want to work at this company?",
        "Where do you see yourself in 5 years?",
        "Describe your greatest technical achievement.",
        "How do you handle tight deadlines and pressure?",
        "Tell me about a time you disagreed with a team member. How did you handle it?",
        "How do you keep your technical skills up to date?",
        "What is your preferred development methodology (Agile, Scrum, Kanban)?",
        "How do you handle code reviews — giving and receiving feedback?",
        "What motivates you as a software engineer?",
        "Describe a time you failed and what you learned from it.",
        "How do you approach working in a remote or distributed team?",
    ],

    # ----------------------------------------------------------
    "Python Developer": [
        # Technical
        "What are Python decorators? Write an example.",
        "Explain Python generators and the yield keyword.",
        "What is the difference between a list and a tuple in Python?",
        "Explain Python virtual environments and why they matter.",
        "How does Python manage memory and garbage collection?",
        "What are lambda functions in Python?",
        "Explain exception handling best practices in Python.",
        "What is the difference between deep copy and shallow copy?",
        "Explain Python modules and packages.",
        "What are Python iterators and how do you create one?",
        "Explain OOP in Python: classes, inheritance, encapsulation, polymorphism.",
        "How does a Python dictionary work internally (hash tables)?",
        "Explain multiprocessing vs multithreading in Python.",
        "What is the difference between Flask and FastAPI?",
        "How do you optimize slow Python code?",
        "What are type hints and why are they useful?",
        "Explain context managers and the `with` statement.",
        "How do you handle API requests in Python using `requests` or `httpx`?",
        "What is `asyncio` and when would you use `async/await` in Python?",
        "Explain list comprehensions, dict comprehensions, and generator expressions.",
        "What is the GIL (Global Interpreter Lock) and how does it affect performance?",
        "Explain Python's `*args` and `**kwargs`.",
        "What are dataclasses in Python and how are they different from regular classes?",
        "Explain metaclasses in Python.",
        "What is `__slots__` and when would you use it?",
        "Explain the difference between `is` and `==` in Python.",
        "What is memoization and how do you implement it in Python?",
        "How do you write and run unit tests with `pytest`?",
        "Explain Pydantic and its role in data validation.",
        "What is SQLAlchemy? Explain ORM vs raw SQL.",
        # Scenario-based
        "You have a Python script running 10x slower than expected. How do you profile and fix it?",
        "How would you design a Python REST API to handle 10,000 requests per second?",
        "You receive malformed JSON from a third-party API. How do you handle it safely?",
        "A memory leak is detected in your long-running Python process. How do you debug it?",
        "How would you implement a rate limiter in Python?",
        "Design a Python function that retries failed API calls with exponential backoff.",
        "How would you handle environment-specific configurations in a Python project?",
        "Explain how you structure a large Python project for maintainability.",
        # HR
        "Tell me about yourself and your Python development experience.",
        "Why do you prefer Python over other programming languages?",
        "Describe your most challenging Python project.",
        "How do you stay updated with new Python versions and features?",
        "Tell me about a time you had to learn a new Python library quickly.",
        "How do you approach code quality and code reviews?",
        "Where do you see yourself in 5 years as a Python developer?",
        "How do you handle working with legacy Python 2 code?",
        "Describe a time you worked on a Python project in a team.",
        "What tools and editors do you use for Python development?",
        "How do you handle disagreements about technical decisions in Python projects?",
        "What motivates you most about Python development?",
    ],

    # ----------------------------------------------------------
    "Java Developer": [
        # Technical
        "Explain JVM architecture and how bytecode is executed.",
        "What is the difference between JDK, JRE, and JVM?",
        "Explain Java garbage collection algorithms (G1, CMS, ZGC).",
        "What are Java interfaces and how do they differ from abstract classes?",
        "Explain inheritance and method overriding in Java.",
        "What is the difference between ArrayList and LinkedList?",
        "Explain Java exception handling: checked vs unchecked exceptions.",
        "What are Java threads and how do you create them?",
        "Explain synchronization, locks, and deadlocks in Java.",
        "How does HashMap work internally in Java?",
        "Explain Java collections framework (List, Set, Map, Queue).",
        "What are Java Streams and how do you use them?",
        "Explain lambda expressions in Java 8+.",
        "What is Spring Boot and what problems does it solve?",
        "Explain dependency injection in Spring.",
        "What is Spring Data JPA and how does it work?",
        "Explain Java memory model (heap, stack, metaspace).",
        "What is the difference between `==` and `.equals()` in Java?",
        "Explain multithreading: ExecutorService, Future, CompletableFuture.",
        "What is the Singleton pattern? How do you implement it thread-safely?",
        "Explain Java generics and wildcards.",
        "What is method overloading vs method overriding?",
        "Explain the `final`, `finally`, and `finalize` keywords.",
        "What is Optional in Java and why is it used?",
        "Explain reactive programming with Spring WebFlux.",
        "What is the difference between `StringBuilder` and `StringBuffer`?",
        "Explain try-with-resources and AutoCloseable.",
        "What is reflection in Java?",
        "Explain Java serialization and deserialization.",
        "How do you write unit tests in Java with JUnit and Mockito?",
        # Scenario-based
        "A Java application is running out of heap memory. How do you diagnose it?",
        "How would you design a thread-safe singleton in Java?",
        "You see a deadlock in production. How do you identify and resolve it?",
        "How would you implement a caching layer in a Spring Boot application?",
        "Design a microservice in Spring Boot that handles user authentication.",
        "How would you optimize a slow SQL query in a Spring Data JPA application?",
        "A REST endpoint is returning inconsistent results. How do you debug it?",
        "Explain how you would migrate a monolith Java application to microservices.",
        # HR
        "Tell me about yourself and your Java experience.",
        "Why do you choose Java for backend development?",
        "Describe your most complex Java project.",
        "How do you stay current with Java updates and the Spring ecosystem?",
        "Tell me about a time you solved a difficult concurrency bug.",
        "How do you approach performance tuning in Java applications?",
        "Where do you see yourself in 5 years as a Java developer?",
        "Describe how you handle code reviews in a Java team.",
        "How do you ensure code quality in Java projects?",
        "What Java frameworks and tools do you use regularly?",
        "Describe a time you worked under tight deadlines on a Java project.",
        "What motivates you about Java development?",
    ],

    # ----------------------------------------------------------
    "AI Engineer": [
        # Technical
        "Explain the difference between AI, Machine Learning, and Deep Learning.",
        "What is a neural network? Explain forward and backward propagation.",
        "What is a transformer model and how does the attention mechanism work?",
        "Explain large language models (LLMs) and how they are trained.",
        "What is prompt engineering? Give examples of effective prompt patterns.",
        "Explain fine-tuning vs. training from scratch for LLMs.",
        "What is RAG (Retrieval-Augmented Generation) architecture?",
        "Explain embeddings and their applications in NLP.",
        "What are attention mechanisms (self-attention, cross-attention, multi-head)?",
        "Explain overfitting and underfitting. How do you prevent each?",
        "What is model evaluation? Explain precision, recall, F1, AUC-ROC.",
        "What are AI agents? Explain the agent loop (perception, reasoning, action).",
        "Explain vector databases and when you would use Pinecone, Weaviate, or Chroma.",
        "How do you deploy ML models to production (REST API, batch, streaming)?",
        "Explain transfer learning and its advantages.",
        "What is generative AI? How does a diffusion model work?",
        "Explain hallucination in AI models. How do you mitigate it?",
        "What is reinforcement learning from human feedback (RLHF)?",
        "Explain the difference between BERT and GPT architectures.",
        "What is LangChain and what problems does it solve?",
        "Explain tokenization in NLP. What are BPE and WordPiece?",
        "What is model quantization and why is it used?",
        "Explain the softmax function and its role in classification.",
        "What are hyperparameters? How do you tune them?",
        "Explain batch normalization and dropout regularization.",
        "What is a knowledge graph and how is it used in AI?",
        "Explain the difference between supervised, unsupervised, and self-supervised learning.",
        "What is zero-shot, one-shot, and few-shot learning?",
        "Explain MLOps and the ML lifecycle (data, train, evaluate, deploy, monitor).",
        "What is model drift and how do you detect and handle it?",
        # Scenario-based
        "You notice an LLM is producing inconsistent answers. How do you improve it?",
        "A customer wants an AI chatbot for their internal documents. Design the architecture.",
        "How would you build a semantic search engine using embeddings?",
        "An AI model performs well in testing but poorly in production. What do you investigate?",
        "How would you evaluate the quality of a RAG pipeline?",
        "Design a pipeline to fine-tune an LLM on domain-specific data.",
        "How would you handle PII (personal data) in an AI training pipeline?",
        "Your inference latency is 5 seconds per request. How do you reduce it?",
        # HR
        "Tell me about yourself and your AI engineering background.",
        "Why are you passionate about AI/ML engineering?",
        "Describe your most impactful AI project.",
        "How do you keep up with the rapidly changing AI landscape?",
        "Tell me about a time an AI model you built failed. What did you learn?",
        "How do you explain complex AI concepts to non-technical stakeholders?",
        "Where do you see AI engineering going in the next 5 years?",
        "How do you balance model performance with compute cost?",
        "Describe your experience working with AI in production environments.",
        "What AI/ML tools and frameworks do you use regularly?",
        "How do you approach AI ethics and responsible AI?",
        "What motivates you most about working in AI engineering?",
    ],

    # ----------------------------------------------------------
    "Machine Learning Engineer": [
        "Explain the machine learning workflow from data collection to deployment.",
        "What is the bias-variance tradeoff?",
        "Explain gradient descent and its variants (SGD, Adam, RMSprop).",
        "What is cross-validation and why is it used?",
        "Explain decision trees and how they handle overfitting.",
        "What is ensemble learning? Explain bagging and boosting.",
        "Explain random forests and how feature importance is calculated.",
        "What is XGBoost and why is it popular for structured data?",
        "Explain support vector machines (SVM) and kernel tricks.",
        "What is principal component analysis (PCA)?",
        "Explain K-means clustering. How do you choose the right K?",
        "What is the curse of dimensionality?",
        "Explain logistic regression and when to use it vs linear regression.",
        "What is regularization? Explain L1 (Lasso) vs L2 (Ridge).",
        "Explain precision, recall, F1 score, and ROC-AUC.",
        "How do you handle imbalanced datasets?",
        "What is feature engineering? Give 5 common techniques.",
        "Explain neural network activation functions (ReLU, Sigmoid, Tanh).",
        "What is a convolutional neural network (CNN) and how does it work?",
        "Explain RNNs, LSTMs, and why transformers replaced them for NLP.",
        "What is the difference between classification and regression?",
        "Explain A/B testing in the context of ML model deployment.",
        "What is SHAP and how is it used for model explainability?",
        "Explain data leakage and how to prevent it.",
        "What is the difference between batch learning and online learning?",
        "Explain the difference between parametric and non-parametric models.",
        "What is time-series forecasting? Explain ARIMA and Prophet.",
        "How do you handle missing values in a dataset?",
        "Explain feature selection techniques.",
        "What is a recommendation system? Explain collaborative filtering.",
        "You have a model with 99% accuracy but it's useless. Why might this happen?",
        "How would you build a fraud detection model?",
        "A model performs great in development but poorly in production. What's wrong?",
        "How do you monitor a deployed ML model?",
        "Design an ML pipeline for customer churn prediction.",
        "How would you handle concept drift in a deployed model?",
        "Your training data has strong temporal patterns. How do you split train/test?",
        "How would you deploy a scikit-learn model as a REST API?",
        "Tell me about yourself and your ML engineering experience.",
        "Describe your most complex ML project end-to-end.",
        "How do you approach data quality issues in ML projects?",
        "How do you collaborate with data scientists and software engineers?",
        "Where do you see ML engineering evolving in the next 3 years?",
        "Tell me about a time an ML model you deployed had unexpected behavior.",
        "How do you communicate model limitations to business stakeholders?",
        "What ML tools and platforms do you use regularly?",
        "How do you decide between building a custom model and using a pretrained one?",
        "Describe your approach to ML experimentation and tracking (MLflow, W&B).",
        "How do you handle privacy and compliance in ML pipelines?",
        "What motivates you about machine learning engineering?",
    ],

    # ----------------------------------------------------------
    "Data Scientist": [
        "Explain the data science workflow from problem definition to deployment.",
        "What is exploratory data analysis (EDA)? What steps do you follow?",
        "Explain hypothesis testing: null hypothesis, p-value, significance level.",
        "What is the difference between correlation and causation?",
        "Explain the central limit theorem.",
        "What is Bayesian inference? How is it different from frequentist statistics?",
        "Explain linear regression assumptions and how to test them.",
        "What is multicollinearity and how do you handle it?",
        "Explain ANOVA and when you would use it.",
        "What is the difference between Type I and Type II errors?",
        "Explain clustering algorithms: K-means, DBSCAN, hierarchical.",
        "How do you evaluate unsupervised learning models?",
        "Explain natural language processing (NLP) techniques you have used.",
        "What is topic modeling? Explain LDA.",
        "Explain the difference between deep learning and traditional ML.",
        "How do you choose between different ML models for a problem?",
        "Explain survival analysis.",
        "What is time-series decomposition (trend, seasonality, residual)?",
        "Explain Shapley values for model interpretability.",
        "What is the difference between mean, median, and mode? When to use each?",
        "Explain standard deviation vs variance.",
        "What are confidence intervals and how do you interpret them?",
        "Explain dimensionality reduction: PCA, t-SNE, UMAP.",
        "What is the difference between a data scientist and an ML engineer?",
        "Explain data pipelines and ETL processes.",
        "How do you handle outliers in a dataset?",
        "What is Simpson's paradox?",
        "Explain chi-square test and when to use it.",
        "How do you measure the success of a data science project?",
        "What is a data dictionary and why is it important?",
        "How would you analyze why a company's revenue dropped last quarter?",
        "Design an experiment to test whether a new UI increases user engagement.",
        "How would you detect fraudulent transactions using data science?",
        "A stakeholder wants 95% accuracy. What do you tell them?",
        "How would you build a customer segmentation model?",
        "How would you handle 3 months of missing sales data?",
        "Your analysis contradicts what the business believes. How do you present it?",
        "How would you determine the ROI of a data science project?",
        "Tell me about yourself and your data science background.",
        "Describe your most impactful data science project.",
        "How do you communicate statistical results to non-technical stakeholders?",
        "What tools do you use for data analysis and visualization?",
        "How do you keep up with new developments in data science?",
        "Tell me about a time your analysis was wrong. What did you learn?",
        "How do you handle ambiguous problem definitions?",
        "Where do you see data science evolving in the next 5 years?",
        "How do you balance exploration vs. delivering results quickly?",
        "Describe a time you collaborated with engineers to put a model in production.",
        "What programming languages do you prefer for data science and why?",
        "What motivates you about data science?",
    ],

    # ----------------------------------------------------------
    "Data Analyst": [
        "Explain the difference between a data analyst and a data scientist.",
        "What SQL queries do you use most often in your daily work?",
        "Explain the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN.",
        "What are window functions in SQL? Give examples.",
        "Explain GROUP BY, HAVING, and their differences from WHERE.",
        "What is a subquery vs a CTE (Common Table Expression)?",
        "Explain normalization in databases (1NF, 2NF, 3NF).",
        "What is data wrangling and what tools do you use?",
        "Explain pivot tables and their use in Excel/Google Sheets.",
        "What is the difference between OLTP and OLAP?",
        "Explain star schema vs snowflake schema in data warehousing.",
        "What is a data warehouse? How is it different from a database?",
        "Explain ETL vs ELT.",
        "What is Tableau/Power BI? How do you choose the right visualization?",
        "Explain KPIs and how you define metrics for a business.",
        "What is data profiling and why is it important?",
        "Explain outlier detection techniques for analytical data.",
        "What is the difference between structured and unstructured data?",
        "Explain cohort analysis.",
        "What is funnel analysis?",
        "Explain A/B testing from an analytical perspective.",
        "What is the difference between mean and median? When does median matter more?",
        "Explain data governance and data quality.",
        "What is a dashboard? How do you design an effective one?",
        "Explain the concept of data lineage.",
        "What are the most common data quality issues you encounter?",
        "Explain how you would calculate customer lifetime value (CLV).",
        "What is retention rate and how do you calculate it?",
        "Explain churn analysis.",
        "How do you handle missing data in analytical datasets?",
        "Sales dropped 20% this month. How do you investigate using data?",
        "How would you build a reporting dashboard for a marketing team?",
        "A manager asks for a metric that you know is misleading. What do you do?",
        "How would you validate data migrated from one system to another?",
        "Design a data model for an e-commerce order tracking system.",
        "How do you prioritize analytics requests from multiple stakeholders?",
        "How would you communicate a finding that contradicts a popular assumption?",
        "How would you automate a recurring report?",
        "Tell me about yourself and your data analysis experience.",
        "Describe a data project where your analysis led to a business decision.",
        "How do you ensure the accuracy of your analyses?",
        "What tools and technologies are in your data analytics toolkit?",
        "Tell me about a time you had to clean a very messy dataset.",
        "How do you communicate complex data findings to non-technical people?",
        "Where do you see data analytics evolving in the next 3-5 years?",
        "How do you handle situations where data is unavailable or incomplete?",
        "Describe your experience with any BI tools.",
        "How do you collaborate with business stakeholders to define requirements?",
        "Tell me about a time you found an unexpected insight in data.",
        "What motivates you about data analysis?",
    ],

    # ----------------------------------------------------------
    "Full Stack Developer": [
        "Explain the difference between frontend and backend development.",
        "What is the MVC architecture pattern?",
        "Explain RESTful API design principles.",
        "What is the difference between session-based and JWT authentication?",
        "Explain how CORS works and how to configure it.",
        "What is GraphQL and how does it differ from REST?",
        "Explain WebSockets and when you would use them over HTTP.",
        "What is server-side rendering (SSR) vs client-side rendering (CSR)?",
        "Explain the difference between SQL and NoSQL. When do you choose each?",
        "What is ORM? Explain pros and cons.",
        "Explain database transactions and ACID properties.",
        "What is Redis and how is it used in a full stack application?",
        "Explain the virtual DOM in React and how reconciliation works.",
        "What is state management? Explain Redux vs Zustand vs Context API.",
        "Explain how to implement pagination in a REST API and frontend.",
        "What is a CDN and how does it improve performance?",
        "Explain the concept of microservices in a full stack context.",
        "What is Docker and how do you use it in a full stack project?",
        "Explain CI/CD and how you set it up for a full stack application.",
        "What are environment variables and how do you manage them?",
        "Explain OAuth 2.0 and how social login (Google/GitHub) works.",
        "What is a reverse proxy? How does Nginx fit into a full stack architecture?",
        "Explain database migrations and why they are important.",
        "What is input validation and sanitization? Why is it critical?",
        "Explain common web security vulnerabilities: XSS, CSRF, SQL injection.",
        "What is the difference between monorepo and polyrepo project structures?",
        "Explain lazy loading and code splitting in frontend applications.",
        "What is an API gateway?",
        "Explain caching strategies for a full stack app (browser, CDN, server, DB).",
        "How do you handle file uploads in a full stack application?",
        "Design a full stack architecture for a real-time chat application.",
        "How would you handle user authentication in a full stack project from scratch?",
        "A page is loading slowly. How do you diagnose and fix it?",
        "Your API is being overloaded. What strategies do you implement?",
        "How would you implement a notification system in a full stack application?",
        "How would you handle database migrations in a production environment?",
        "How do you manage secrets and API keys in a full stack project?",
        "Design a scalable full stack architecture for 1 million users.",
        "Tell me about yourself and your full stack development experience.",
        "Describe your most complex full stack project.",
        "How do you decide which tech stack to use for a new project?",
        "How do you stay updated with both frontend and backend technologies?",
        "Tell me about a time you had to debug a cross-cutting issue across the stack.",
        "How do you handle tight deadlines across both frontend and backend tasks?",
        "Where do you see full stack development evolving?",
        "How do you approach code reviews for both frontend and backend code?",
        "Describe your experience with Agile/Scrum in a full stack team.",
        "What development tools and workflows do you rely on daily?",
        "How do you ensure accessibility (a11y) in the applications you build?",
        "What motivates you about full stack development?",
    ],

    # ----------------------------------------------------------
    "Frontend Developer": [
        "Explain the box model in CSS.",
        "What is the difference between `display: flex` and `display: grid`?",
        "Explain CSS specificity and the cascade.",
        "What is the difference between `em`, `rem`, `px`, `%`, and `vw/vh`?",
        "Explain the critical rendering path in a browser.",
        "What is the virtual DOM and how does React use it?",
        "Explain React hooks: useState, useEffect, useContext, useMemo, useCallback.",
        "What is the difference between controlled and uncontrolled components in React?",
        "Explain React component lifecycle.",
        "What is prop drilling and how do you solve it?",
        "Explain CSS animations and transitions.",
        "What is CSS preprocessor (Sass/LESS) and why use it?",
        "What is responsive design? Explain mobile-first vs desktop-first.",
        "Explain Flexbox axis, justify-content, align-items, align-self.",
        "What is the difference between `==` and `===` in JavaScript?",
        "Explain the JavaScript event loop and call stack.",
        "What are JavaScript closures?",
        "Explain async/await and Promises in JavaScript.",
        "What is the difference between `var`, `let`, and `const`?",
        "Explain the DOM and how JavaScript manipulates it.",
        "What is event delegation in JavaScript?",
        "Explain `this` keyword in JavaScript.",
        "What is a higher-order function? Give examples.",
        "Explain lazy loading of images and JavaScript modules.",
        "What are Web Vitals (LCP, FID, CLS) and how do you improve them?",
        "Explain code splitting and dynamic imports in a React application.",
        "What is accessibility (a11y)? Give 5 best practices.",
        "Explain CORS from a frontend perspective.",
        "What is localStorage vs sessionStorage vs cookies?",
        "Explain service workers and Progressive Web Apps (PWA).",
        "A React component is re-rendering too often. How do you optimize it?",
        "How would you implement infinite scroll in a React application?",
        "Design a reusable component library architecture.",
        "Your website scores 40 on Google Lighthouse. How do you improve it?",
        "How would you implement dark mode in a web application?",
        "How do you handle error boundaries in React?",
        "How would you implement a debounce or throttle function?",
        "How do you manage state in a large React application?",
        "Tell me about yourself and your frontend development experience.",
        "Describe your most visually impressive or complex UI project.",
        "How do you approach cross-browser compatibility issues?",
        "How do you stay updated with rapidly changing frontend technologies?",
        "Tell me about a time you improved the performance of a web application.",
        "How do you collaborate with UI/UX designers?",
        "How do you prioritize frontend tasks?",
        "Where do you see frontend development evolving?",
        "How do you handle feedback on your UI implementation?",
        "What tools and extensions do you use daily for frontend development?",
        "Describe your experience with testing frontend code (Jest, Cypress).",
        "What motivates you about frontend development?",
    ],

    # ----------------------------------------------------------
    "Backend Developer": [
        "Explain the request-response lifecycle in a web server.",
        "What is the difference between REST, GraphQL, and gRPC?",
        "Explain HTTP methods: GET, POST, PUT, PATCH, DELETE.",
        "What are HTTP status codes? Explain 200, 201, 400, 401, 403, 404, 500.",
        "Explain middleware in backend frameworks.",
        "What is database connection pooling and why is it important?",
        "Explain the N+1 query problem and how to solve it.",
        "What is database sharding and when do you use it?",
        "Explain ACID transactions with a real-world example.",
        "What is eventual consistency in distributed systems?",
        "Explain rate limiting and how to implement it.",
        "What is API versioning and what strategies do you use?",
        "Explain caching layers: in-memory (Redis), CDN, database query cache.",
        "What is a message broker (RabbitMQ, Kafka)? When do you use it?",
        "Explain the difference between optimistic and pessimistic locking.",
        "What is a webhook? How does it differ from polling?",
        "Explain JWT structure (header, payload, signature) and security.",
        "What is idempotency and why does it matter in APIs?",
        "Explain database replication (master-slave, master-master).",
        "What is a reverse proxy? What does Nginx do in a backend setup?",
        "Explain the 12-factor app methodology.",
        "What is observability? Explain logging, metrics, and tracing.",
        "Explain blue-green deployment and canary releases.",
        "What is a circuit breaker pattern?",
        "Explain task queues and background job processing.",
        "What is the difference between horizontal and vertical scaling?",
        "Explain SQL query optimization techniques.",
        "What are stored procedures and when should you avoid them?",
        "Explain index types: B-tree, hash, full-text.",
        "What is the CAP theorem and how does it affect backend design?",
        "Design a backend API for a social media feed (pagination, likes, comments).",
        "How would you handle 10,000 concurrent requests on a single backend server?",
        "Your API response time increased from 50ms to 3 seconds. Investigate.",
        "How would you design a file upload service to handle large files?",
        "How would you implement soft delete in a database?",
        "Design a backend for a food delivery app.",
        "How would you handle distributed transactions across microservices?",
        "How do you secure a REST API against common attacks?",
        "Tell me about yourself and your backend development experience.",
        "Describe your most complex backend system.",
        "How do you approach designing a new API from scratch?",
        "How do you ensure your APIs are backward-compatible?",
        "Tell me about a performance issue you solved in a backend system.",
        "How do you handle database migrations in production?",
        "Where do you see backend development evolving?",
        "How do you collaborate with frontend developers?",
        "How do you ensure the reliability of your backend services?",
        "What backend frameworks and tools do you prefer?",
        "Describe your experience with containerization (Docker, Kubernetes).",
        "What motivates you about backend development?",
    ],

    # ----------------------------------------------------------
    "React Developer": [
        "What is React and what problems does it solve?",
        "Explain the virtual DOM and how React's reconciliation algorithm works.",
        "What are React hooks? Explain useState, useEffect, useRef, useMemo.",
        "What is the difference between class components and functional components?",
        "Explain React component lifecycle phases.",
        "What is JSX and how does it compile?",
        "Explain React Context API and when to use it vs Redux.",
        "What is Redux? Explain actions, reducers, and store.",
        "What is React Query (TanStack Query) and how does it handle server state?",
        "Explain controlled vs uncontrolled components.",
        "What is the difference between `useCallback` and `useMemo`?",
        "Explain React.memo and when to use it.",
        "What are React Portals?",
        "Explain error boundaries in React.",
        "What is React.lazy() and Suspense?",
        "Explain higher-order components (HOC) and render props patterns.",
        "What is prop drilling and how do you solve it?",
        "Explain custom hooks and give 3 examples you've built.",
        "What is the key prop in React and why is it important?",
        "Explain how React handles forms (controlled inputs, useForm).",
        "What is Zustand and how does it compare to Redux?",
        "Explain React Router (v6): BrowserRouter, Routes, Route, useNavigate.",
        "What is code splitting in React? Explain dynamic imports.",
        "Explain how you would implement infinite scroll in React.",
        "What are the React testing utilities? Explain React Testing Library.",
        "Explain Next.js features: SSR, SSG, ISR, App Router.",
        "What is the difference between SPA and MPA?",
        "Explain how to optimize React app performance.",
        "What is Storybook and how is it used for component development?",
        "Explain Tailwind CSS integration with a React project.",
        "A React component is re-rendering 20 times per second. How do you debug it?",
        "Design a reusable table component with sorting, filtering, and pagination.",
        "How do you handle global loading and error states in a large React app?",
        "How would you implement real-time notifications in a React app?",
        "How do you manage forms with complex validation in React?",
        "How would you structure a large-scale React application?",
        "How do you handle authentication flows in a React SPA?",
        "How do you implement a theme switcher (dark/light mode) in React?",
        "Tell me about yourself and your React development experience.",
        "Describe your most complex React project.",
        "How do you stay updated with the React ecosystem?",
        "Tell me about a time you improved performance in a React application.",
        "How do you approach testing in React applications?",
        "How do you collaborate with backend teams when APIs aren't ready?",
        "Where do you see React evolving?",
        "How do you handle disagreements about component design in a team?",
        "Describe your experience with TypeScript in React projects.",
        "What development tools do you use daily for React development?",
        "How do you handle accessibility in React applications?",
        "What motivates you about React development?",
    ],

    # ----------------------------------------------------------
    "Node.js Developer": [
        "Explain Node.js and the event-driven, non-blocking I/O model.",
        "What is the Node.js event loop? Explain all its phases.",
        "Explain the difference between `process.nextTick()`, `setImmediate()`, and `setTimeout()`.",
        "What is the V8 engine and how does it execute JavaScript?",
        "Explain streams in Node.js (Readable, Writable, Duplex, Transform).",
        "What is the difference between `require()` and `import` in Node.js?",
        "Explain Express.js middleware chain.",
        "What is clustering in Node.js and when do you use it?",
        "Explain the difference between `fs.readFile` and `fs.createReadStream`.",
        "What is CORS in Node.js? How do you configure it in Express?",
        "Explain JWT authentication in a Node.js/Express app.",
        "What is Mongoose? How does it relate to MongoDB?",
        "Explain error handling in Express (synchronous vs async errors).",
        "What is the purpose of `package.json` and `package-lock.json`?",
        "Explain npm vs yarn vs pnpm.",
        "What are environment variables and how do you use them in Node.js?",
        "Explain rate limiting in Node.js APIs.",
        "What is WebSocket? How do you implement it with Socket.io?",
        "Explain worker threads in Node.js.",
        "What is the difference between SQL (PostgreSQL) and NoSQL (MongoDB) in Node projects?",
        "Explain caching with Redis in a Node.js application.",
        "What is GraphQL and how do you implement it in Node.js?",
        "Explain microservices architecture in Node.js.",
        "What is Fastify and how does it compare to Express?",
        "Explain database connection pooling with pg or Sequelize.",
        "What is NestJS and what problems does it solve?",
        "Explain file uploads in Node.js using Multer.",
        "What is the child_process module and when do you use it?",
        "Explain graceful shutdown in a Node.js application.",
        "What is PM2 and how does it help in production?",
        "Your Node.js API is leaking memory. How do you detect and fix it?",
        "Design a real-time collaborative document editor backend using Node.js.",
        "How would you implement a job queue with Bull/BullMQ in Node.js?",
        "How do you handle file processing for large CSV uploads?",
        "Design a Node.js microservice architecture for an e-commerce platform.",
        "How would you implement multi-tenancy in a Node.js application?",
        "Your Express.js server crashes under load. How do you investigate?",
        "How do you implement end-to-end testing for a Node.js REST API?",
        "Tell me about yourself and your Node.js experience.",
        "Describe your most complex Node.js project.",
        "How do you manage dependencies and security in Node.js projects?",
        "Tell me about a performance optimization you made in Node.js.",
        "How do you structure a large Node.js project?",
        "Where do you see Node.js evolving in the backend ecosystem?",
        "How do you handle API versioning in Node.js?",
        "How do you approach error monitoring in production Node.js apps?",
        "Describe your experience with TypeScript in Node.js projects.",
        "What testing frameworks do you use for Node.js?",
        "How do you collaborate with frontend teams when building APIs?",
        "What motivates you about Node.js development?",
    ],

    # ----------------------------------------------------------
    "Android Developer": [
        "Explain the Android application lifecycle (Activity and Fragment).",
        "What is the difference between Activity and Fragment?",
        "Explain ViewModel and LiveData in Android.",
        "What is the Android Jetpack library? Name key components.",
        "Explain Room database and how it compares to SQLite.",
        "What is Retrofit and how do you use it for API calls?",
        "Explain RecyclerView vs ListView.",
        "What is the difference between Service, IntentService, and JobScheduler?",
        "Explain BroadcastReceiver and ContentProvider.",
        "What is the Android manifest file?",
        "Explain layouts in Android: ConstraintLayout, LinearLayout, RelativeLayout.",
        "What is Kotlin Coroutines? Explain suspend functions.",
        "Explain Kotlin Flow vs LiveData.",
        "What is Hilt/Dagger dependency injection in Android?",
        "Explain the MVVM architecture pattern in Android.",
        "What is Jetpack Compose? How is it different from XML layouts?",
        "Explain how push notifications work in Android (FCM).",
        "What is WorkManager and when do you use it?",
        "Explain how to handle configuration changes (screen rotation) in Android.",
        "What is the difference between SharedPreferences and Room?",
        "Explain Navigation Component in Android.",
        "What is Glide/Picasso and how does image loading work?",
        "Explain Android permissions (normal, dangerous, signature).",
        "What is ProGuard/R8 and why is it used?",
        "Explain Android build flavors and build types.",
        "What is ADB and how do you use it for debugging?",
        "Explain memory management in Android (avoid memory leaks).",
        "What is ANR (Application Not Responding) and how do you prevent it?",
        "Explain how to implement offline support in an Android app.",
        "What is the Play Store publishing process?",
        "Your Android app crashes on a specific device. How do you debug it?",
        "Design an Android architecture for a food delivery application.",
        "How would you implement real-time chat in an Android app?",
        "Your app has a high battery consumption. How do you optimize it?",
        "How would you implement biometric authentication in Android?",
        "How do you handle API errors gracefully in an Android app?",
        "How would you implement an image gallery with offline support?",
        "How do you ensure your Android app is accessible?",
        "Tell me about yourself and your Android development experience.",
        "Describe your most complex Android application.",
        "How do you approach testing (unit, integration, UI) in Android?",
        "Tell me about a difficult bug you fixed in Android.",
        "How do you keep up with Android/Jetpack updates?",
        "How do you handle backward compatibility in Android?",
        "Where do you see Android development evolving?",
        "How do you collaborate with backend developers and designers?",
        "How do you manage app size and APK optimization?",
        "What tools do you use daily for Android development?",
        "Describe your experience publishing to the Google Play Store.",
        "What motivates you about Android development?",
    ],

    # ----------------------------------------------------------
    "DevOps Engineer": [
        "Explain CI/CD and its benefits.",
        "What is Docker? Explain images, containers, and volumes.",
        "What is Kubernetes? Explain pods, deployments, and services.",
        "Explain blue-green deployment vs canary release.",
        "What is Infrastructure as Code (IaC)? Explain Terraform.",
        "What is Ansible and how does it differ from Terraform?",
        "Explain the difference between horizontal and vertical scaling.",
        "What is a load balancer? Explain ALB vs NLB.",
        "Explain auto-scaling in cloud environments.",
        "What is Nginx and how do you configure it as a reverse proxy?",
        "Explain monitoring and observability: Prometheus, Grafana, ELK stack.",
        "What is log aggregation and how do you implement it?",
        "Explain distributed tracing (Jaeger, Zipkin).",
        "What is GitOps and how does ArgoCD work?",
        "Explain Helm charts in Kubernetes.",
        "What is a service mesh (Istio, Linkerd)?",
        "Explain secrets management (HashiCorp Vault, Kubernetes Secrets).",
        "What is the difference between VM and container?",
        "Explain Docker networking (bridge, host, overlay).",
        "What is a multi-stage Docker build and why use it?",
        "Explain Kubernetes resource requests and limits.",
        "What is a Kubernetes Ingress controller?",
        "Explain rolling updates and rollbacks in Kubernetes.",
        "What is a Dockerfile and explain common instructions.",
        "What is Jenkins and how does a CI pipeline work?",
        "Explain GitHub Actions and how to set up a workflow.",
        "What is SRE (Site Reliability Engineering)?",
        "Explain SLO, SLA, and SLI.",
        "What is chaos engineering?",
        "Explain disaster recovery strategies (RTO, RPO).",
        "Production is down at 2 AM. Walk me through your incident response.",
        "Design a CI/CD pipeline for a microservices application.",
        "How would you implement zero-downtime deployment?",
        "Your Kubernetes pod keeps crashing. How do you debug it?",
        "How would you secure a Kubernetes cluster?",
        "How do you handle database migrations in a CI/CD pipeline?",
        "Design a monitoring strategy for a high-traffic web application.",
        "How would you reduce Docker image size from 2GB to under 200MB?",
        "Tell me about yourself and your DevOps engineering experience.",
        "Describe the most complex infrastructure you have managed.",
        "How do you handle on-call incidents?",
        "Tell me about a time you improved deployment reliability.",
        "How do you balance speed of delivery vs stability?",
        "Where do you see DevOps/Platform Engineering evolving?",
        "How do you communicate infrastructure changes to development teams?",
        "How do you approach cost optimization in cloud environments?",
        "Describe your experience with cloud platforms (AWS/GCP/Azure).",
        "How do you ensure security and compliance in your pipelines?",
        "What DevOps tools are you most proficient with?",
        "What motivates you about DevOps engineering?",
    ],

    # ----------------------------------------------------------
    "Cloud Engineer": [
        "Explain the difference between IaaS, PaaS, and SaaS.",
        "Compare AWS, GCP, and Azure at a high level.",
        "Explain AWS core services: EC2, S3, RDS, Lambda, VPC.",
        "What is a VPC (Virtual Private Cloud)? Explain subnets, routing tables.",
        "Explain security groups vs NACLs in AWS.",
        "What is IAM? Explain roles, policies, and the principle of least privilege.",
        "Explain serverless computing and AWS Lambda.",
        "What is AWS ECS vs EKS vs Fargate?",
        "Explain object storage (S3): durability, availability, storage classes.",
        "What is CloudFront and how does a CDN work?",
        "Explain auto-scaling groups and launch templates in AWS.",
        "What is Elastic Load Balancing (ALB, NLB, CLB)?",
        "Explain AWS RDS vs DynamoDB vs Aurora.",
        "What is AWS SQS vs SNS vs EventBridge?",
        "Explain multi-region architecture and failover.",
        "What is Terraform? Explain resources, providers, and state.",
        "Explain AWS CloudFormation vs Terraform.",
        "What is AWS CloudWatch? Explain metrics, logs, alarms.",
        "Explain AWS Cost Explorer and billing optimization.",
        "What is a VPN vs Direct Connect vs VPC Peering?",
        "Explain disaster recovery strategies (backup, pilot light, warm standby, multi-site).",
        "What is AWS Config and AWS Trusted Advisor?",
        "Explain Kubernetes on AWS (EKS) vs on GCP (GKE).",
        "What is Cloud Storage lifecycle policy?",
        "Explain data encryption at rest and in transit in cloud.",
        "What is a NAT gateway and why is it used?",
        "Explain AWS Step Functions.",
        "What is AWS API Gateway?",
        "Explain AWS Secrets Manager vs Parameter Store.",
        "What is FinOps and how do you implement cloud cost optimization?",
        "Design a highly available, fault-tolerant architecture on AWS.",
        "How would you migrate a monolith application to the cloud?",
        "An EC2 instance is unreachable. How do you troubleshoot it?",
        "How would you implement multi-region failover for a web application?",
        "Design a serverless data pipeline on AWS.",
        "How would you reduce AWS costs by 40%?",
        "How would you implement a secure network architecture on AWS?",
        "How do you handle compliance (HIPAA, GDPR) in cloud environments?",
        "Tell me about yourself and your cloud engineering experience.",
        "Describe the largest cloud infrastructure you have built.",
        "How do you stay updated with cloud provider announcements?",
        "Tell me about a time you resolved a major cloud outage.",
        "How do you approach cloud cost optimization?",
        "Where do you see cloud computing evolving?",
        "How do you collaborate with development teams on cloud architecture?",
        "What cloud certifications do you hold or are pursuing?",
        "How do you ensure security and compliance in cloud projects?",
        "Describe your experience with multi-cloud or hybrid cloud.",
        "What is your approach to cloud automation?",
        "What motivates you about cloud engineering?",
    ],

    # ----------------------------------------------------------
    "Cyber Security Engineer": [
        "Explain the CIA triad: Confidentiality, Integrity, Availability.",
        "What is the OWASP Top 10? Explain at least 5 vulnerabilities.",
        "Explain SQL injection and how to prevent it.",
        "What is cross-site scripting (XSS)? Explain stored vs reflected XSS.",
        "What is CSRF and how do you prevent it?",
        "Explain how HTTPS/TLS works (certificates, handshake, encryption).",
        "What is the difference between symmetric and asymmetric encryption?",
        "Explain hashing vs encryption. Which is used for passwords and why?",
        "What is a firewall? Explain stateful vs stateless firewall.",
        "What is an IDS vs IPS?",
        "Explain the difference between penetration testing and vulnerability assessment.",
        "What is social engineering? Give 3 examples.",
        "Explain phishing and spear phishing.",
        "What is multi-factor authentication (MFA)? Explain TOTP.",
        "What is OAuth 2.0 and OpenID Connect?",
        "Explain zero-trust security architecture.",
        "What is SIEM and how is it used in security operations?",
        "Explain the MITRE ATT&CK framework.",
        "What is a buffer overflow attack?",
        "Explain man-in-the-middle (MITM) attacks.",
        "What is privilege escalation?",
        "Explain DNS poisoning and how to prevent it.",
        "What is a VPN and how does it provide security?",
        "Explain container security best practices.",
        "What is secrets management and why is it critical?",
        "Explain the principle of least privilege.",
        "What is a CVE and CVSS score?",
        "Explain static application security testing (SAST) vs DAST.",
        "What is PKI (Public Key Infrastructure)?",
        "Explain incident response phases (identification, containment, eradication, recovery).",
        "A server was compromised. Walk me through your incident response.",
        "How would you secure a REST API from common attacks?",
        "A developer checked an API key into a public GitHub repo. What do you do?",
        "How would you implement security scanning in a CI/CD pipeline?",
        "How would you conduct a security audit of a web application?",
        "A user reports they received a suspicious email from your domain. Investigate.",
        "How would you implement defense-in-depth for a cloud application?",
        "How do you handle a ransomware attack?",
        "Tell me about yourself and your cybersecurity background.",
        "Describe your experience with penetration testing or security audits.",
        "How do you stay current with emerging security threats?",
        "Tell me about a security vulnerability you discovered and fixed.",
        "How do you communicate security risks to non-technical stakeholders?",
        "Where do you see cybersecurity evolving in the next 5 years?",
        "How do you build a security-first culture in a development team?",
        "What security frameworks and compliance standards have you worked with?",
        "Describe your experience with security tools (Nmap, Burp Suite, Wireshark).",
        "How do you approach threat modeling?",
        "What motivates you about cybersecurity?",
        "How do you balance security requirements with business deadlines?",
    ],

    # ----------------------------------------------------------
    "SQL Developer": [
        "Explain the difference between DDL, DML, DCL, and TCL in SQL.",
        "What are the types of SQL JOINs? Give examples for each.",
        "Explain window functions with examples (RANK, DENSE_RANK, ROW_NUMBER, LEAD, LAG).",
        "What is a CTE (Common Table Expression)? How does it differ from a subquery?",
        "Explain database normalization (1NF, 2NF, 3NF, BCNF).",
        "What is denormalization and when do you use it?",
        "Explain indexes: types, how they work, and when to avoid them.",
        "What is a query execution plan and how do you read it?",
        "Explain the difference between UNION and UNION ALL.",
        "What is the difference between DELETE, TRUNCATE, and DROP?",
        "Explain stored procedures: advantages and disadvantages.",
        "What are triggers in SQL?",
        "Explain views vs materialized views.",
        "What is a transaction? Explain ACID properties with examples.",
        "Explain isolation levels (READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE).",
        "What are dirty reads, phantom reads, and non-repeatable reads?",
        "Explain the difference between a clustered and non-clustered index.",
        "What is a primary key vs unique key vs foreign key?",
        "Explain COALESCE vs ISNULL vs NULLIF.",
        "What are aggregate functions? Explain GROUP BY and HAVING.",
        "Explain the difference between INNER JOIN and LEFT JOIN with NULL handling.",
        "What is a recursive CTE? Give an example.",
        "Explain partitioning in SQL databases.",
        "What is database sharding?",
        "Explain the difference between OLTP and OLAP databases.",
        "What is a star schema? How does it differ from a snowflake schema?",
        "Explain query optimization techniques.",
        "What is a deadlock in SQL and how do you resolve it?",
        "Explain the difference between row-level and table-level locking.",
        "What are temporary tables and table variables?",
        "You have a query that returns results in 45 seconds. Optimize it.",
        "Write a SQL query to find the second-highest salary in a table.",
        "Write a SQL query to find duplicate records in a table.",
        "How would you pivot data (rows to columns) in SQL?",
        "How would you find the top 3 products by sales in each category?",
        "How would you detect gaps in a sequence in a table?",
        "Design a database schema for an e-commerce platform.",
        "How would you implement soft delete in SQL?",
        "Tell me about yourself and your SQL development experience.",
        "Describe your most complex SQL query or project.",
        "How do you approach database performance optimization?",
        "How do you handle large-scale data migrations in SQL?",
        "Tell me about a time you debugged a complex SQL performance issue.",
        "How do you ensure data integrity in your databases?",
        "Where do you see database technology evolving?",
        "How do you collaborate with application developers on database design?",
        "How do you document your database schemas?",
        "What SQL databases and tools do you work with regularly?",
        "How do you handle database backups and disaster recovery?",
        "What motivates you about SQL development?",
    ],

    # ----------------------------------------------------------
    "QA Engineer": [
        "Explain the software testing lifecycle (STLC).",
        "What is the difference between verification and validation?",
        "Explain the different types of software testing.",
        "What is the difference between functional and non-functional testing?",
        "Explain unit testing vs integration testing vs end-to-end testing.",
        "What is regression testing and when do you perform it?",
        "Explain smoke testing vs sanity testing.",
        "What is exploratory testing?",
        "Explain performance testing: load, stress, and spike testing.",
        "What is a test case? What are its key components?",
        "What is a test plan? What does it contain?",
        "Explain the bug lifecycle (defect life cycle).",
        "What information should a good bug report contain?",
        "Explain boundary value analysis and equivalence partitioning.",
        "What is test coverage and how do you measure it?",
        "Explain Selenium WebDriver and how it works.",
        "What is Page Object Model (POM) in Selenium?",
        "Explain API testing using Postman or Rest Assured.",
        "What is the difference between black-box, white-box, and grey-box testing?",
        "Explain shift-left testing.",
        "What is continuous testing in a CI/CD pipeline?",
        "Explain test-driven development (TDD) and behavior-driven development (BDD).",
        "What is Cucumber and how does it relate to BDD?",
        "Explain Cypress vs Selenium.",
        "What is load testing? Explain JMeter.",
        "What is a mock and a stub in testing?",
        "Explain cross-browser testing strategies.",
        "What is mobile application testing? Explain Appium.",
        "Explain accessibility testing.",
        "What is security testing and what tools do you use?",
        "You find a critical bug 1 hour before a production release. What do you do?",
        "How do you test an API that has no documentation?",
        "Design a test strategy for a payment gateway integration.",
        "How do you prioritize which tests to automate?",
        "How would you test a login form with valid, invalid, and edge case inputs?",
        "How do you handle flaky tests in an automation suite?",
        "How would you build an automation framework from scratch?",
        "How do you measure the effectiveness of your test suite?",
        "Tell me about yourself and your QA engineering experience.",
        "Describe your most complex testing project.",
        "How do you collaborate with developers to improve quality?",
        "Tell me about a critical bug you found that saved the project.",
        "How do you handle situations where developers push back on bug reports?",
        "How do you balance thorough testing with fast delivery timelines?",
        "Where do you see QA engineering evolving with AI?",
        "How do you keep your automation suite maintainable?",
        "Describe your experience with test management tools (Jira, TestRail).",
        "How do you approach risk-based testing?",
        "What testing frameworks and tools do you use regularly?",
        "What motivates you about QA engineering?",
    ],

    # ----------------------------------------------------------
    "UI/UX Designer": [
        "Explain the difference between UI and UX design.",
        "What is the design thinking process? Explain all 5 stages.",
        "What is a user persona and how do you create one?",
        "Explain user journey mapping.",
        "What is wireframing vs prototyping?",
        "Explain the difference between low-fidelity and high-fidelity prototypes.",
        "What is usability testing? How do you conduct it?",
        "Explain the 10 usability heuristics by Jakob Nielsen.",
        "What is accessibility (a11y) in UI/UX? Explain WCAG guidelines.",
        "What is responsive design? How do you design for multiple screen sizes?",
        "Explain the Gestalt principles in design.",
        "What is information architecture (IA)?",
        "Explain card sorting and tree testing.",
        "What is A/B testing in UX? Give an example.",
        "Explain the difference between serif and sans-serif fonts.",
        "What is a design system? What are its components?",
        "Explain color theory: primary, secondary, complementary colors.",
        "What is the 60-30-10 color rule?",
        "Explain whitespace and its importance in design.",
        "What is visual hierarchy and how do you create it?",
        "Explain microinteractions and their importance.",
        "What is affordance in UX design?",
        "Explain the difference between flat design and material design.",
        "What is dark mode design? What are the key considerations?",
        "Explain iconography best practices.",
        "What tools do you use for UI/UX design (Figma, Sketch, Adobe XD)?",
        "Explain how you hand off designs to developers.",
        "What is atomic design methodology?",
        "Explain mobile-first design principles.",
        "What are the key differences between designing for iOS vs Android?",
        "A user says the app is confusing. How do you diagnose and fix the UX issue?",
        "How would you redesign a checkout flow to reduce cart abandonment?",
        "How do you design an onboarding experience for a complex product?",
        "How would you conduct user research for a completely new product?",
        "How would you present a design decision to stakeholders who disagree?",
        "How do you design for users with disabilities?",
        "How would you approach designing a dashboard for non-technical users?",
        "How do you validate that a design solution solves the user problem?",
        "Tell me about yourself and your UI/UX design background.",
        "Walk me through your design process for your best project.",
        "How do you handle design feedback and iteration?",
        "Tell me about a time your design decision was wrong. How did you fix it?",
        "How do you collaborate with product managers and developers?",
        "How do you balance aesthetics with usability?",
        "Where do you see UI/UX design evolving with AI?",
        "How do you manage multiple projects and design deadlines?",
        "How do you stay inspired and updated in design?",
        "Describe your experience building or contributing to a design system.",
        "How do you measure the success of a UX design?",
        "What motivates you about UI/UX design?",
    ],

    # ----------------------------------------------------------
    "Product Manager": [
        "Explain the role of a Product Manager in a tech company.",
        "What is a product roadmap? How do you create one?",
        "Explain the difference between product vision and product strategy.",
        "What is a PRD (Product Requirements Document)?",
        "Explain Agile and Scrum methodology from a PM perspective.",
        "What is the difference between product manager and project manager?",
        "Explain how you prioritize features using frameworks (RICE, MoSCoW, Kano).",
        "What is a North Star metric?",
        "Explain OKRs (Objectives and Key Results).",
        "What is product-market fit? How do you measure it?",
        "Explain user stories and acceptance criteria.",
        "What is MVP (Minimum Viable Product)? How do you define it?",
        "Explain the build-measure-learn loop (Lean Startup).",
        "What is a go-to-market (GTM) strategy?",
        "Explain how you conduct competitive analysis.",
        "What is Net Promoter Score (NPS)? How do you use it?",
        "Explain cohort analysis from a product perspective.",
        "What is DAU/MAU and what does it tell you about a product?",
        "Explain A/B testing and statistical significance.",
        "What is customer journey mapping?",
        "Explain how you gather and prioritize user feedback.",
        "What is technical debt from a PM perspective? How do you handle it?",
        "Explain how you work with engineering, design, and data teams.",
        "What is a sprint review vs sprint retrospective?",
        "Explain how you handle feature requests from sales and customers.",
        "What is a KPI and how do you select the right metrics for a product?",
        "Explain the jobs-to-be-done (JTBD) framework.",
        "What is a product hypothesis and how do you test it?",
        "Explain how you would sunset a product feature.",
        "What is the difference between B2B and B2C product management?",
        "Your product's engagement dropped 30% last week. Walk me through your analysis.",
        "How would you prioritize: a feature 60% of users want vs a bug affecting 5%?",
        "How do you handle a situation where engineering says a feature is impossible?",
        "How would you launch a new feature to 1 million users?",
        "A competitor just launched a feature your users have been requesting. What do you do?",
        "How would you determine whether to build vs buy a feature?",
        "How do you make a product decision with incomplete data?",
        "Design a product strategy for a new food delivery app entering a competitive market.",
        "Tell me about yourself and your product management experience.",
        "Describe your most successful product launch.",
        "How do you say 'no' to a stakeholder's feature request?",
        "Tell me about a time a product decision you made was wrong.",
        "How do you manage relationships between engineering and design?",
        "How do you keep a team motivated during a difficult sprint?",
        "Where do you see product management evolving with AI?",
        "How do you handle conflict between what users want and what the business needs?",
        "Describe your experience with data-driven product decisions.",
        "How do you communicate product strategy to the whole company?",
        "What tools do you use regularly as a product manager?",
        "What motivates you about product management?",
    ],
}


# ============================================================
# OFFLINE EVALUATION ENGINE
# ============================================================

# Role-specific evaluation insights for unique feedback generation
ROLE_FEEDBACK_GUIDANCE = {
    "Software Engineer": {
        "focus": "system architecture, algorithms, object-oriented design, SOLID principles, and testing strategies",
        "strength": "Demonstrated core software engineering principles and architectural awareness",
        "improvement": "Deepen your explanation of system design trade-offs, Big O complexity, and design patterns"
    },
    "Python Developer": {
        "focus": "Pythonic idioms, decorators, generators, asyncio, virtual environments, and frameworks (FastAPI/Flask)",
        "strength": "Showed familiarity with Python-specific language features and development practices",
        "improvement": "Focus on Python memory management, GIL implications, typing, and async concurrency models"
    },
    "Java Developer": {
        "focus": "JVM internals, Spring ecosystem, multithreading synchronization, collections framework, and clean OOP",
        "strength": "Demonstrated knowledge of Java framework structures and object-oriented paradigms",
        "improvement": "Elaborate further on JVM garbage collection tuning, Spring Boot dependency injection, and concurrency locks"
    },
    "AI Engineer": {
        "focus": "transformer models, text embeddings, RAG pipelines, LLM fine-tuning, prompt optimization, and vector DBs",
        "strength": "Displayed understanding of modern generative AI workflows and model architectures",
        "improvement": "Practice explaining RAG evaluation metrics, context window limitations, and hallucination mitigation"
    },
    "Machine Learning Engineer": {
        "focus": "feature engineering, bias-variance tradeoff, model validation, hyperparameter tuning, and MLOps",
        "strength": "Showcased practical understanding of the end-to-end machine learning pipeline",
        "improvement": "Strengthen explanations of concept drift detection, loss function choices, and model deployment pipelines"
    },
    "Data Scientist": {
        "focus": "statistical hypothesis testing, exploratory data analysis, predictive modeling, and business insights",
        "strength": "Demonstrated analytical thinking and data-driven problem-solving capability",
        "improvement": "Enhance your explanations of statistical assumptions, model interpretability (SHAP/LIME), and experimental design"
    },
    "Data Analyst": {
        "focus": "advanced SQL queries, data wrangling, KPI metrics tracking, visualization tools, and reporting",
        "strength": "Showed solid proficiency in data aggregation, SQL concepts, and business reporting logic",
        "improvement": "Focus on window function optimization, data pipeline integrity, and translating data findings into executive summaries"
    },
    "Full Stack Developer": {
        "focus": "end-to-end application architecture, REST/GraphQL APIs, database state management, and frontend UI flow",
        "strength": "Exhibited cross-stack awareness connecting frontend interactions with backend services",
        "improvement": "Work on detailing state synchronization strategies, security headers (CORS/CSRF), and microservice boundaries"
    },
    "Frontend Developer": {
        "focus": "modern CSS/Flexbox/Grid, DOM manipulation, responsive layouts, web accessibility (WCAG), and performance",
        "strength": "Demonstrated understanding of user interface structure and frontend layout mechanics",
        "improvement": "Deepen your knowledge of browser critical rendering paths, Core Web Vitals optimization, and state management"
    },
    "Backend Developer": {
        "focus": "API scalability, database indexing, caching strategies (Redis), message queues, and rate limiting",
        "strength": "Displayed solid grasp of server-side application logic and API integration design",
        "improvement": "Focus on distributed transaction handling, database connection pooling, and circuit breaker patterns"
    },
    "React Developer": {
        "focus": "React hook optimizations, Virtual DOM reconciliation, state management (Redux/Zustand), and lazy loading",
        "strength": "Demonstrated component-driven design thinking and React state flow comprehension",
        "improvement": "Practice articulating custom hook design, memoization trade-offs, and re-render prevention strategies"
    },
    "Node.js Developer": {
        "focus": "event loop phases, non-blocking asynchronous I/O, Express middleware, streams, and npm ecosystem",
        "strength": "Showed clear familiarity with Node.js event-driven runtime mechanics and API creation",
        "improvement": "Elaborate more on memory leak debugging, cluster module usage, and worker thread concurrency"
    },
    "Android Developer": {
        "focus": "Kotlin coroutines, Jetpack components (ViewModel/Room), Activity lifecycle, and UI responsiveness",
        "strength": "Exhibited good understanding of native Android development and application components",
        "improvement": "Focus on memory leak prevention, background work scheduling with WorkManager, and Jetpack Compose state"
    },
    "DevOps Engineer": {
        "focus": "CI/CD pipelines, Docker containerization, Kubernetes orchestration, Infrastructure as Code, and monitoring",
        "strength": "Showcased awareness of deployment automation and continuous delivery workflows",
        "improvement": "Deepen explanations of zero-downtime deployment strategies, cluster security, and observability stacks"
    },
    "Cloud Engineer": {
        "focus": "cloud security posture (IAM/VPC), serverless architecture, multi-region failover, and cost optimization",
        "strength": "Demonstrated foundational cloud infrastructure concepts and multi-service management",
        "improvement": "Practice detailing cloud networking isolation, Terraform state management, and FinOps cost strategies"
    },
    "Cyber Security Engineer": {
        "focus": "OWASP Top 10 mitigation, threat modeling, network encryption, zero-trust architecture, and incident response",
        "strength": "Displayed strong security awareness and vulnerability mitigation principles",
        "improvement": "Focus on detailing incident response containment procedures, static/dynamic security testing (SAST/DAST), and TLS handshakes"
    },
    "SQL Developer": {
        "focus": "complex SQL JOINs, CTEs, window functions, index optimization, execution plans, and ACID normalization",
        "strength": "Demonstrated strong database query formulation and relational schema knowledge",
        "improvement": "Work on explaining query execution plan analysis, deadlock resolution, and partitioning techniques"
    },
    "QA Engineer": {
        "focus": "test automation frameworks, edge case identification, STLC bug lifecycle, API testing, and regression suites",
        "strength": "Exhibited meticulous testing logic and quality assurance methodology",
        "improvement": "Deepen explanations of flaky test mitigation, continuous testing pipelines, and performance stress testing"
    },
    "UI/UX Designer": {
        "focus": "user research methodologies, wireframing, interactive prototyping, visual hierarchy, and accessibility",
        "strength": "Demonstrated user-centered design thinking and interface clarity focus",
        "improvement": "Focus on articulating heuristic evaluation principles, design system component tokens, and usability test metrics"
    },
    "Product Manager": {
        "focus": "feature prioritization (RICE/Kano), product roadmap design, KPI/OKR tracking, and stakeholder alignment",
        "strength": "Displayed strategic product vision and structured decision-making processes",
        "improvement": "Elaborate further on data-driven metric decomposition, build-vs-buy analysis, and managing technical debt priorities"
    }
}


# Role-specific keywords for offline scoring
GENERAL_TECH_TERMS = [
    "algorithm", "api", "architecture", "async", "backend", "cache", "ci/cd", "cloud",
    "database", "debug", "deployment", "design", "devops", "docker", "frontend", "framework",
    "git", "interface", "kubernetes", "memory", "microservices", "object", "optimization",
    "performance", "piping", "process", "python", "rest", "security", "server", "service",
    "software", "sql", "state", "system", "testing", "thread", "unit", "user", "data", "code"
]

ROLE_KEYWORDS = {
    "Software Engineer": ["sdlc", "oop", "polymorphism", "rest", "design pattern", "indexing", "multithreading", "git", "solid", "microservices", "cache", "load balancing", "docker", "testing"],
    "Python Developer": ["decorator", "generator", "yield", "virtualenv", "gil", "lambda", "asyncio", "flask", "fastapi", "pydantic", "sqlalchemy", "dict", "tuple", "list", "pytest"],
    "Java Developer": ["jvm", "jdk", "jre", "garbage collection", "spring", "jpa", "arraylist", "hashmap", "multithreading", "maven", "gradle", "singleton", "interface", "checked exception"],
    "Full Stack Developer": ["frontend", "backend", "rest", "graphql", "database", "react", "node", "state", "api", "auth", "middleware", "express", "sql", "css", "html"],
    "Frontend Developer": ["css", "html", "javascript", "dom", "flexbox", "grid", "responsive", "react", "vue", "accessibility", "wcag", "state", "props", "web vitals"],
    "Backend Developer": ["api", "rest", "database", "sql", "nosql", "cache", "redis", "kafka", "rabbitmq", "scalability", "microservices", "indexing", "authentication", "rate limit"],
    "React Developer": ["jsx", "hooks", "usestate", "useeffect", "usememo", "usecallback", "redux", "zustand", "virtual dom", "reconciliation", "props", "component", "router"],
    "Node.js Developer": ["event loop", "non-blocking", "express", "npm", "async", "await", "stream", "buffer", "commonjs", "module", "middleware", "cluster", "v8"],
    "Android Developer": ["kotlin", "java", "jetpack", "activity", "fragment", "viewmodel", "room", "coroutines", "lifecycle", "compose", "intent", "workmanager", "manifest"],
    "AI Engineer": ["llm", "transformer", "rag", "embeddings", "prompt", "fine-tuning", "vector", "agent", "langchain", "attention", "generative", "neural", "python"],
    "Machine Learning Engineer": ["bias", "variance", "gradient descent", "cross-validation", "decision tree", "xgboost", "pca", "kmeans", "hyperparameter", "pipeline", "scikit", "feature"],
    "Data Scientist": ["eda", "hypothesis", "p-value", "regression", "statistics", "clustering", "pandas", "numpy", "seaborn", "shap", "time series", "classification", "python"],
    "Data Analyst": ["sql", "join", "group by", "having", "cte", "window function", "tableau", "power bi", "excel", "dashboard", "etl", "kpi", "pivot", "chart"],
    "SQL Developer": ["query", "join", "cte", "window function", "index", "execution plan", "acid", "stored procedure", "trigger", "normalization", "transaction", "primary key"],
    "DevOps Engineer": ["ci/cd", "pipeline", "docker", "kubernetes", "terraform", "ansible", "jenkins", "git", "bash", "monitoring", "prometheus", "grafana", "yaml"],
    "Cloud Engineer": ["aws", "azure", "gcp", "iam", "vpc", "s3", "ec2", "lambda", "serverless", "terraform", "cloudformation", "networking", "security group"],
    "Cyber Security Engineer": ["owasp", "vulnerability", "encryption", "firewall", "siem", "zero trust", "penetration", "authentication", "tls", "ssl", "incident", "threat"],
    "QA Engineer": ["automation", "selenium", "cypress", "pytest", "bug", "test case", "regression", "smoke", "api testing", "postman", "jira", "unit test", "stlc"],
    "UI/UX Designer": ["figma", "wireframe", "prototype", "user research", "usability", "heuristic", "accessibility", "visual hierarchy", "color theory", "persona", "design system"],
    "Product Manager": ["roadmap", "prd", "rice", "kano", "okr", "kpi", "mvp", "agile", "scrum", "user story", "backlog", "stakeholder", "sprint", "prioritization"]
}


def offline_evaluate(questions: list, answers: list, role: str) -> dict:
    """
    Offline evaluation engine that scores answers without Gemini.
    Uses answer length, keyword matching, and technical depth.
    Provides role-specific dynamic feedback and handles invalid/empty answers gracefully.
    """
    role_info = ROLE_FEEDBACK_GUIDANCE.get(role, {
        "focus": f"core competencies and best practices in {role}",
        "strength": f"Demonstrated technical awareness relevant to the {role} role",
        "improvement": f"Practice expanding your technical depth and providing concrete examples for {role} questions"
    })

    # Prepare question-wise feedback structure
    question_feedback = []

    if not questions or not answers:
        return {
            "score": 0,
            "feedback": f"Please provide valid answers. No responses were submitted for your {role} interview session.",
            "strengths": [f"Initiated the {role} interview session"],
            "improvements": [f"Please enter detailed technical responses into the answer fields for {role}"],
            "question_feedback": []
        }

    # Filter valid answers (more than just empty whitespace)
    valid_answers = [a.strip() for a in answers if a and len(a.strip()) > 0]
    total_words = sum(len(a.split()) for a in valid_answers)

    # 1. Zero answers provided
    if len(valid_answers) == 0:
        for i, q in enumerate(questions):
            question_feedback.append({
                "question_num": i + 1,
                "question": q,
                "answer": "No response provided",
                "score": 0,
                "feedback": "Skipped. No answer was submitted for evaluation."
            })
        return {
            "score": 0,
            "feedback": f"Please provide valid answers for the questions. Your submission was completely empty, so we could not evaluate your technical proficiency for the {role} position.",
            "strengths": [f"Initiated the {role} assessment session"],
            "improvements": [
                f"Ensure you type complete, structured answers before clicking Submit Interview",
                f"Review key technical topics in {role_info['focus']} before re-attempting"
            ],
            "question_feedback": question_feedback
        }

    # 2. Insufficient / single-word filler responses
    if total_words < 15:
        for i, (q, a) in enumerate(zip(questions, answers)):
            ans_clean = a.strip() if a else ""
            question_feedback.append({
                "question_num": i + 1,
                "question": q,
                "answer": ans_clean if ans_clean else "No response provided",
                "score": 10 if ans_clean else 0,
                "feedback": f"Response too brief ({len(ans_clean.split())} words). Please elaborate with complete technical concepts."
            })
        return {
            "score": 10,
            "feedback": f"Please provide valid, detailed answers. The responses provided for your {role} interview were too brief or incomplete to properly evaluate your technical skills.",
            "strengths": [f"Attempted to answer some questions in the {role} interview"],
            "improvements": [
                f"Provide full explanations for each question (aim for 40–100+ words per answer)",
                f"Incorporate domain-specific terminology regarding {role_info['focus']}",
                "Use concrete examples from your past projects or study to back up your claims"
            ],
            "question_feedback": question_feedback
        }

    role_keywords = [k.lower() for k in ROLE_KEYWORDS.get(role, [])]
    general_terms = [t.lower() for t in GENERAL_TECH_TERMS]

    total_score = 0
    answered_count = 0
    strong_answers = []
    weak_answers = []

    for i, (question, answer) in enumerate(zip(questions, answers)):
        ans_clean = answer.strip() if answer else ""
        if not ans_clean:
            question_feedback.append({
                "question_num": i + 1,
                "question": question,
                "answer": "No response provided",
                "score": 0,
                "feedback": "Skipped. No answer was submitted for this question."
            })
            continue

        answered_count += 1
        answer_lower = ans_clean.lower()
        words = answer_lower.split()
        word_count = len(words)
        q_num = i + 1

        # --- Length Score (0-30 points) ---
        if word_count >= 100:
            length_score = 30
        elif word_count >= 60:
            length_score = 22
        elif word_count >= 30:
            length_score = 14
        elif word_count >= 10:
            length_score = 7
        else:
            length_score = 2

        # --- Role Keyword Matching (0-35 points) ---
        matched_keywords = [k for k in role_keywords if k in answer_lower]
        keyword_score = min(35, len(matched_keywords) * 7)

        # --- General Technical Terms (0-20 points) ---
        general_matched = [t for t in general_terms if t in answer_lower]
        general_score = min(20, len(general_matched) * 4)

        # --- Confidence/Completeness Score (0-15 points) ---
        confidence_indicators = [
            "for example", "such as", "because", "therefore", "this means",
            "in other words", "specifically", "in practice", "in summary",
            "the reason", "which means", "this helps", "this allows", "this ensures"
        ]
        confidence_count = sum(1 for ind in confidence_indicators if ind in answer_lower)
        confidence_score = min(15, confidence_count * 5)

        answer_score = length_score + keyword_score + general_score + confidence_score

        if answer_score >= 60:
            strong_answers.append(q_num)
            q_fb = f"Strong technical answer! Covers key concepts well ({word_count} words)."
        elif answer_score < 30:
            weak_answers.append(q_num)
            q_fb = f"Needs improvement. Elaborate further with technical specifics and domain keywords for {role}."
        else:
            q_fb = f"Good response ({word_count} words). Consider adding practical code/architecture trade-off details."

        question_feedback.append({
            "question_num": q_num,
            "question": question,
            "answer": ans_clean,
            "score": min(100, answer_score),
            "feedback": q_fb
        })

        total_score += answer_score

    # Normalize score
    final_score = round((total_score / (len(questions) * 100)) * 100) if questions else 0
    final_score = max(12, min(98, final_score))

    if answered_count == len(questions):
        final_score = min(98, final_score + 5)

    if final_score >= 80:
        overall_feedback = (
            f"Outstanding technical performance for the {role} role! Your answers demonstrated comprehensive "
            f"mastery of {role_info['focus']}. You explained complex concepts clearly with appropriate technical depth "
            f"and industry-standard terminology."
        )
    elif final_score >= 65:
        overall_feedback = (
            f"Strong performance in your {role} assessment. You showed a solid understanding of core concepts "
            f"relating to {role_info['focus']}. To reach top-tier scores, include more specific architectural trade-offs "
            f"and hands-on code or project examples."
        )
    elif final_score >= 50:
        overall_feedback = (
            f"Fair attempt at the {role} interview. You demonstrated foundational knowledge of {role}, but several answers "
            f"lacked technical precision regarding {role_info['focus']}. Focused review on core topics will boost your performance."
        )
    else:
        overall_feedback = (
            f"Your performance indicates that further preparation is recommended for the {role} position. "
            f"Focus on strengthening your core understanding of {role_info['focus']} and practicing detailed written answers."
        )

    strengths = []
    if answered_count == len(questions):
        strengths.append(f"Answered all {len(questions)} questions in the {role} evaluation")
    strengths.append(role_info["strength"])
    if strong_answers:
        strengths.append(f"Demonstrated high technical accuracy on {len(strong_answers)} specific question(s)")
    if len([a for a in answers if len(a.strip().split()) >= 40]) >= 3:
        strengths.append(f"Provided detailed, well-explained responses highlighting {role} domain knowledge")

    improvements = []
    if len(questions) - answered_count > 0:
        improvements.append(f"Complete all unanswered questions ({len(questions) - answered_count} skipped in this round)")
    improvements.append(role_info["improvement"])
    if weak_answers:
        improvements.append(f"Elaborate with deeper detail on question(s) {', '.join(map(str, weak_answers[:3]))}")
    if final_score < 75:
        improvements.append(f"Incorporate more industry terminology related to {role_info['focus']}")

    return {
        "score": final_score,
        "feedback": overall_feedback,
        "strengths": strengths[:4],
        "improvements": improvements[:4],
        "question_feedback": question_feedback
    }


# ============================================================
# GENERATE QUESTIONS — Local bank first, Gemini fallback
# ============================================================

def generate_questions(role: str, experience: str) -> list:
    """
    Returns a full pool of 50+ questions for the given role.
    Priority: 1) Local bank  2) Gemini  3) Default fallback
    """
    local_questions = QUESTION_BANK.get(role, []).copy()

    if len(local_questions) >= 20:
        random.shuffle(local_questions)
        return local_questions

    if _gemini_client:
        try:
            prompt = f"""Generate exactly 50 professional interview questions for the role "{role}".
Experience Level: {experience}

Include a mix of:
- Technical questions (25)
- HR/behavioral questions (10)
- Scenario-based questions (10)
- Beginner, intermediate, and advanced level questions (5 each category)

Return ONLY a valid JSON array of strings. No markdown, no extra text.
Example format:
["Question 1", "Question 2", "Question 3"]"""

            response = _gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            text = response.text.strip()
            text = re.sub(r"```(?:json)?", "", text).strip()
            generated = json.loads(text)
            if isinstance(generated, list) and len(generated) >= 10:
                random.shuffle(generated)
                return generated
        except Exception as e:
            print(f"[WARN] Gemini question generation failed: {e}")

    print(f"[INFO] Using default fallback questions for role: {role}")
    fallback = QUESTION_BANK.get("Software Engineer", []).copy()
    random.shuffle(fallback)
    return fallback


# ============================================================
# EVALUATE ANSWERS — Gemini first, offline fallback
# ============================================================

def evaluate_answers(questions: list, answers: list, role: str) -> dict:
    """
    Evaluates interview answers.
    Priority: 1) Gemini AI  2) Offline evaluator
    """
    valid_answers = [a.strip() for a in answers if a and len(a.strip()) > 0]
    total_words = sum(len(a.split()) for a in valid_answers)

    if len(valid_answers) == 0 or total_words < 15:
        return offline_evaluate(questions, answers, role)

    if _gemini_client:
        try:
            qa_pairs = "\n".join(
                f"Q{i+1}: {q}\nA{i+1}: {a if a else '[No answer]'}"
                for i, (q, a) in enumerate(zip(questions, answers))
            )

            prompt = f"""You are an expert technical interviewer evaluating a candidate specifically for the role of "{role}".

Interview Q&A:
{qa_pairs}

Evaluate the candidate's performance thoroughly and provide highly role-specific feedback for a "{role}".
If answers are invalid, empty, or gibberish, return score 0 and feedback starting with "Please provide valid answers...".

Return ONLY valid JSON in exactly this format (no markdown, no extra text):
{{
  "score": <integer 0-100>,
  "feedback": "<2-3 sentence overall feedback tailored specifically to {role}>",
  "strengths": ["<role-specific strength 1>", "<role-specific strength 2>", "<role-specific strength 3>"],
  "improvements": ["<role-specific improvement 1>", "<role-specific improvement 2>", "<role-specific improvement 3>"],
  "question_feedback": [
    {{
      "question_num": 1,
      "question": "<question>",
      "answer": "<candidate answer>",
      "score": <integer 0-100>,
      "feedback": "<1-2 sentence evaluation of candidate's response>"
    }}
  ]
}}"""

            response = _gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            text = response.text.strip()
            text = re.sub(r"```(?:json)?", "", text).strip()
            result = json.loads(text)

            if all(k in result for k in ["score", "feedback", "strengths", "improvements"]):
                result["score"] = int(result.get("score", 0))
                # Ensure question_feedback is present
                if "question_feedback" not in result or not result["question_feedback"]:
                    q_fb = []
                    for i, (q, a) in enumerate(zip(questions, answers)):
                        ans_c = a.strip() if a else ""
                        q_fb.append({
                            "question_num": i + 1,
                            "question": q,
                            "answer": ans_c if ans_c else "No response provided",
                            "score": 80 if len(ans_c.split()) > 30 else 40 if ans_c else 0,
                            "feedback": f"Evaluated for {role} role."
                        })
                    result["question_feedback"] = q_fb
                return result

        except Exception as e:
            print(f"[WARN] Gemini evaluation failed, using offline evaluator: {e}")

    return offline_evaluate(questions, answers, role)