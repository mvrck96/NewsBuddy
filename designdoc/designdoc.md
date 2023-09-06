# ML System Design Doc - NewsBuddy

## 1. Goals and prerequisites
### 1.1. Product development motivation  

Our bank recently created an investment platform for registered users to buy and sell financial products. Being a new solution provider on the market, our product management team compiles a list of features to help the platform gain popularity among users.
They believe that NewsBuddy - financial news sentiment analysis feature - has to be on this list for the following reasons:  
- Usability studies show that users want to have more near-real-time insights in order to make financial decisions. Such an indicator can be used as a risk mitigation tool when users try to buy products with high negative sentiment. Overall, the sentiment indicator feature will improve user experience.
- Some of our competitors already have a comparable feature. We believe it is wise to keep up with them not to miss out even at the expense of the development costs
- If the model at the core of the feature proves reliable, its output can be re-used as an additional input into other ML systems in our banking app.
- We want to invest into our ML teams’ professional development in the NLP domain as surveys show the application field will grow and such competences will be needed across the organisation

### 1.2. Business requirements and constraints  
**Core setup**: *after the first iteration*, the service can access recent financial news sources, attribute them to products in our portfolio and produce a probability distribution among three classes (positive, negative or neutral) for each news item.   
*After the second iteration*, the system produces an aggregated general sentiment label taking into account all received and processed news over a given time period N (internally configurable parameter).

**Requirements and constraints for the ML team:**
- Availability
  - All calculations must be done each day before the start of the trading window.
  - Maximum load capacity of YYY news per minute
- Accuracy:
  -   Minimum accuracy of YYY% on the hold-out data set
- Reliability:
  - The service must not crash or output obvious nonsense in case of any technical issues (e.g. with parsing raw data)  
- Scalability:
  - It is possible to scale the number of financial products, news sources
- Explainability:
  - Documentation
  - Internally, individual news classification results are available for debugging and backtracking
  - Basic frontend and dashboards (for internal access, debug, demos and usability interviews)
- Inputs and outputs:
  - The service must accept textual news in English language related to our TOP-10 products by popularity
- Budget:
  - For development
  - Inference and infrastructure costs 

**Requirements and constraints handled by other teams:**
- Regulatory compliance 
- User interface and customization
- Integration with other systems’ components



### 1.3. Project Scope 

**Primary:**
- Create data injection, pre-processing, feature generation and training\testing pipelines
- Create an orchestration environment for scheduled run of the pipelines 
- Develop or integrate off-the-shelf 3-class classification model for single news piece sentiment analysis
- Front-end (for internal testing and demos)
- Testing and validation:
  - Performance on historical data
  - Stress testing
- Create deployment infrastructure
  - CI/CD
- Documentation

**Secondary:**
- In-house labelling framework \ labelled news items
- Business analysis and reporting on historical data

**Out of scope:**
- Non-financial news or other market data except news articles
- Financial products advice or price prediction



### 1.4. Solution Prerequisites 
- Access to relevant data sources, labelled (reference) data 
- Tech infrastructure: storage, computing resources
- Software and services: github,...
- Domain expertise of the development team 
- Functional and non-functional requirements 
- Communication plan


## 2. Methodology
### 2.1. Problem Statement  

- Multi-class text classification on short to middle size texts

### 2.2. Solution Algorithm

### 2.3.  Stages of Problem Solving
  
## 3. Test Run  
### 3.1. Test Run Evaluation
  
### 3.2. Success  
    
### 3.3. Preparation  

## 4. Deployment    
### 4.1. Solution Architecture
    
### 4.2. Infrastructure and Scaling 
  
### 4.3. System Requirements  
    
### 4.4. System Security  
    
### 4.5. Data Safety   
  
### 4.6. Costs
  
### 4.5. Integration points  
  
### 4.6. Risks
  
