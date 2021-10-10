"""

"""

from pdf2docx import parse
from typing import Tuple

from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from rake_nltk import Rake

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from fuzzywuzzy import fuzz

from spacy.matcher import PhraseMatcher
from collections import Counter

import docx2txt
import pandas as pd
import spacy

import logging

nlp = spacy.load("en_core_web_sm-3.1.0")
r = Rake()

class Resume_aid:

    def resume_processing(self, file_path):
        try:
            self.resume = docx2txt.process(file_path)
            self.text_resume = str(self.resume)
            self.cv_content = ""
            for c in self.resume:
                self.cv_content += c.lower().replace("'","")
            
            # return [text_resume,cv_content]
        except:
            logging.error("Resume could not be read.")

    def job_desc_processing(self, job_content):
        """
        
        """
        try:
            self.job_content = job_content.lower().replace("'","")
            #return job_content

        except:
            logging.error("Job Description could not be read.")

    def cosine_score(self):
        """
        
        """
        try:
            text_list = [self.text_resume, self.job_content]
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(text_list)
            match_percent = cosine_similarity(count_matrix)[0][1]*100
            match_percent = round(match_percent,2)
            logging.info(f"Resume match = {str(match_percent)}%")
            return match_percent

        except:
            logging.error("Scoring issues.")

    def phrase_matching(self):
        """

        """
        try:
            matcher = PhraseMatcher(nlp.vocab)
            self.terms = keywords(self.job_content, ratio=0.25).split('\n')
            patterns = [nlp.make_doc(t) for t in self.terms]
            matcher.add("Spec", patterns)

            doc = nlp(self.text_resume)
            self.match_keywords = []
            matches = matcher(doc)
            for match_id, start, end in matches:
                span = doc[start:end]
                if len(span.text)>3:
                    self.match_keywords.append(span.text)

        except:
            logging.error("Phrase Matching issues.")


    def count_match(self):
        try:
            count_er = Counter(self.match_keywords)

            self.count_act = Counter()
            self.count_act.update({x:0 for x in self.terms})
            self.count_act.update(self.match_keywords)

            return [*count_er]

        except:
            logging.error("Counter object incorrectly intialized.")
    
    def display_match(self):
        try:
            df = pd.DataFrame.from_dict(self.count_act, orient="index").reset_index()
            df = df.rename(columns={'index':'Term', 0:'Count in Resume'})
            
            return (df[df["Count in Resume"]>0])
        
        except:
            logging.error("Loading Pandas Dataframe.")

    def keywords_rake(self, text):
        try:
            keyword = {}
            r.extract_keywords_from_text(text)
            keyword['ranked phrases'] = r.get_ranked_phrases_with_scores()
            return keyword

        except:
            logging.error("Rake phrasing issue.")

    def keyword_score_job(self):
        self.keywords_jb = self.keywords_rake(self.job_content)
        job_score = {}
        for item in self.keywords_jb['ranked phrases'][:10]:
            job_score.update({item[1]: str(round(item[0],2))})
        return job_score 

    def keyword_score_cv(self):
        self.keywords_cv = self.keywords_rake(self.cv_content)
        cv_score = {}
        for item in self.keywords_cv['ranked phrases'][:10]:
            cv_score.update({item[1]: str(round(item[0],2))}) 
        return cv_score
        
    def importance_score(self):
        sims = []
        phrases = []
        for key in self.keywords_jb['ranked phrases']:
            rec={}
            rec['importance'] = key[0]
            texts = key[1]
            sims=[]
            avg_sim=0
            for cvkey in self.keywords_cv['ranked phrases']:
                cvtext = cvkey[1]
                sims.append(fuzz.ratio(texts, cvtext))
                #sims.append(lev.ratio(texts.lower(),cvtext.lower()))
                #sims.append(jaccard_similarity(texts,cvtext))
            count=0
            for s in sims:
                count=count+s
                avg_sim = count/len(sims)
                rec['similarity'] = avg_sim
                rec['text'] = texts
            phrases.append(rec)
        phrase_match = pd.DataFrame(phrases)
        return phrase_match.sort_values(by=["importance"], ascending=False)[:20]



def convert_pdf2docx(input_file: str, output_file: str, pages: Tuple = None):
    """Converts pdf to docx"""
    try:
        if pages:
            pages = [int(i) for i in list(pages) if i.isnumeric()]
        result = parse(pdf_file=input_file,
                    docx_with_path=output_file, pages=pages)
        summary = {
            "File": input_file, "Pages": str(pages), "Output File": output_file
        }
        # Printing Summary
        #logging.info("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
        return result
    except: 
        logging.error("File cannot be converted to docx.")
