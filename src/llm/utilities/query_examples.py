examples = [
    # Basic Information Queries
    {
        "question": "Who is Arghya Bandyopadhyay?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}}) RETURN p
        """
    },
    {
        "question": "Who is Arghya Banerjee?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}}) RETURN p
        """
    },
    {
        "question": "Who is Arghya?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}}) RETURN p
        """
    },
    {
        "question": "Can I have Arghya Bandyopadhyay's LinkedIn profile?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}}) RETURN p.linkedin
        """
    },
    {
        "question": "Where is Arghya Bandyopadhyay located?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}}) RETURN p.location
        """
    },

    # Education Queries
    {
        "question": "What institutions did Arghya attend?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EDUCATION]->(e:education) RETURN e.institute
        """
    },
    {
        "question": "What did Arghya study in 10th grade?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EDUCATION]->(e:education) 
            WHERE e.degree CONTAINS "10 CBSE" RETURN e.institute
        """
    },
    {
        "question": "Where did Arghya study for his bachelor's degree?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EDUCATION]->(e:education {{degree: "B. Tech"}}) RETURN e.institute, e.field_of_study
        """
    },
    {
        "question": "What subjects did Arghya study during his 10+2?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EDUCATION]->(e:education {{degree: "10+2 CBSE"}}) RETURN e.field_of_study
        """
    },
    {
        "question": "What grades did Arghya achieve in his education?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EDUCATION]->(e:education) RETURN e.institute, e.degree, e.grade
        """
    },

    # Experience Queries
    {
        "question": "What work experience does Arghya have?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience) RETURN exp.title, exp.organisation_name, exp.location, exp.start_date, exp.end_date
        """
    },
    {
        "question": "What was Arghya's role at Thoughtworks?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience {{organisation_name: "Thoughtworks"}}) RETURN exp.title, exp.skills
        """
    },
    {
        "question": "List all volunteer positions Arghya held.",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience {{employment_type: "Volunteer"}}) RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
        """
    },
    {
        "question": "What were the key skills Arghya used as an Application Developer?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience {{title: "Application Developer"}}) RETURN exp.skills
        """
    },

    # Certification and Skills Queries
    {
        "question": "What certifications does Arghya hold?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_CERTIFICATION]->(c:certifications) RETURN c.name, c.issue_date, c.credential_url
        """
    },
    {
        "question": "Has Arghya completed any certifications in Neo4j?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_CERTIFICATION]->(c:certifications) WHERE c.skills CONTAINS "Neo4j" RETURN c.name, c.issue_date
        """
    },
    {
        "question": "What skills does Arghya have?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:IS_SKILLED]->(s:skills) RETURN s.name
        """
    },
    {
        "question": "Which certifications did Arghya achieve in 2022?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_CERTIFICATION]->(c:certifications) WHERE c.issue_date CONTAINS "2022" RETURN c.name, c.credential_url
        """
    },

    # Language Proficiency
    {
        "question": "Which languages does Arghya speak?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:SPEAKS]->(l:language) RETURN l.language, l.proficiency
        """
    },
    {
        "question": "What is Arghya's proficiency in Bengali?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:SPEAKS]->(l:language {{language: "Bengali"}}) RETURN l.proficiency
        """
    },

    # Project Queries
    {
        "question": "What projects has Arghya worked on?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects) RETURN pr.project_name, pr.date, pr.description
        """
    },
    {
        "question": "What skills were used in the 'Content Based Music Recommendation' project?",
        "query": """
            MATCH (pr:projects {{project_name: "Content Based Music Recommendation"}})-[:REQUIRED_SKILL]->(s:skills) RETURN s.name
        """
    },
    {
        "question": "Describe the project 'Dictionary API' by Arghya.",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects {{project_name: "Dictionary API"}}) RETURN pr.description, pr.skills, pr.link
        """
    },
    {
        "question": "What recent projects has Arghya completed?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects) RETURN pr.project_name, pr.date ORDER BY pr.date DESC LIMIT 5
        """
    },

    # Honors and Recommendations
    {
        "question": "What awards has Arghya received?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:RECEIVED_AWARD]->(h:honour_and_awards) RETURN h.title, h.associate_with, h.issue_date
        """
    },
    {
        "question": "Who recommended Arghya and what did they say?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_RECOMMENDATION]->(rec:recommendations) RETURN rec.recommender_name, rec.message
        """
    },
    {
        "question": "Has Arghya received any recommendations for teamwork?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_RECOMMENDATION]->(rec:recommendations) WHERE rec.message CONTAINS "teamwork" RETURN rec.recommender_name, rec.message
        """
    },

    # Blog Queries
    {
        "question": "What blogs has Arghya written?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:AUTHORED]->(b:blog) RETURN b.title, b.link, b.published_date
        """
    },
    {
        "question": "Tell me about Arghya's latest blog post.",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:AUTHORED]->(b:blog) RETURN b.title, b.link, b.published_date ORDER BY b.published_date DESC LIMIT 1
        """
    }
]
