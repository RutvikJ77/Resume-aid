# Resume-aid




### Inspiration
Resumes are a vital point in getting your desired job and making one that can help you get that first stage of the interview is very important and at times confusing because there is this gatekeeper Applicant Tracking system aka ATS which searches for keywords from the job description and gives a score to your resume before it gets to the recruiter. Having faced this issue of no response loop from a recruiter I searched about it until I found out about ATS and then it clicked to develop something which will help many job seekers.

### What it does
It takes the user resume and converts it into a document file(.docx) further processing it through the doc2text library and then the spacy library is used for removing the stop words and a resume score is provided using cosine similarity. It provides a simple way for the user to evaluate their resumes against the job descriptions.

### How we built it
It is built using:
- Streamlit 
- Spacy 
- sklearn
- doc2text
- Rake NLTK
- pymupdf

#### Checkout the [demo working video](https://youtu.be/wvI_6pCdz0w)


