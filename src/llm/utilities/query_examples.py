person = [
    {
        "question": "Who is Arghya Bandyopadhyay?",
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
]

education = [
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
    {
        "question": "What are all the degrees Arghya has completed, ordered by year?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EDUCATION]->(e:education)
            WHERE e.end_date IS NOT NULL AND e.end_date <> ""
            WITH e, apoc.date.parse(e.end_date, 'ms', 'MMMM yyyy') AS parsed_end_date
            RETURN e.degree, e.institute, e.start_date, e.end_date
            ORDER BY coalesce(parsed_end_date, apoc.date.parse("December 9999", 'ms', 'MMMM yyyy')) ASC
        """
    },
    {
        "question": "What was Arghya's academic progression starting from high school?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EDUCATION]->(e:education)
            WHERE e.end_date IS NOT NULL AND e.end_date <> ""
            WITH e, apoc.date.parse(e.end_date, 'ms', 'MMMM yyyy') AS parsed_end_date
            RETURN e.degree, e.institute, e.start_date, e.end_date
            ORDER BY coalesce(parsed_end_date, apoc.date.parse("December 9999", 'ms', 'MMMM yyyy')) ASC
        """
    },
]

experience = [
    {
        "question": "What work experience does Arghya have?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience) RETURN exp.title, exp.organisation_name, exp.location, exp.start_date, exp.end_date
        """
    },
    {
        "question": "What is Arghya's role at Thoughtworks?",
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
    {
        "question": "What was Arghya's first job?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
            ORDER BY exp.start_date ASC
            LIMIT 1
        """
    },
    {
        "question": "What is Arghya's current role?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.end_date IS NULL OR exp.end_date = ""
            RETURN exp.title, exp.organisation_name, exp.start_date
        """
    },
    {
        "question": "Can you summarize Arghya's career journey in brief?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.start_date IS NOT NULL AND exp.start_date <> ""
            WITH exp, 
                 apoc.date.parse(exp.start_date, 'ms', 'MMMM yyyy') AS parsed_date
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
            ORDER BY parsed_date DESC
        """
    },
    {
        "question": "What experience did Arghya have between 2018 and 2021?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.start_date IS NOT NULL AND exp.start_date <> "" AND exp.end_date IS NOT NULL AND exp.end_date <> ""
            WITH exp, 
                 apoc.date.parse(exp.start_date, 'ms', 'MMMM yyyy') AS parsed_start_date,
                 apoc.date.parse(exp.end_date, 'ms', 'MMMM yyyy') AS parsed_end_date
            WHERE parsed_start_date >= apoc.date.parse("January 2021", 'ms', 'MMMM yyyy') AND
                  parsed_end_date <= apoc.date.parse("December 2022", 'ms', 'MMMM yyyy')
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date;
        """
    },
    {
        "question": "What is Arghya currently doing and which projects is he involved in?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE coalesce(exp.end_date, "") = ""
            OPTIONAL MATCH (p)-[:WORKED_ON_PROJECT]->(pr:projects)
            RETURN exp.title AS Current_Role, exp.organisation_name, collect(pr.project_name) AS Ongoing_Projects
        """
    },
    {
        "question": "What are Arghya's experiences before February 2023?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.end_date IS NOT NULL AND exp.end_date <> ""
            WITH exp, apoc.date.parse(exp.end_date, 'ms', 'MMMM yyyy') AS parsed_end_date
            WHERE parsed_end_date < apoc.date.parse("February 2023", 'ms', 'MMMM yyyy')
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
        """
    },
    {
        "question": "What are Arghya's experiences before 2023?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.end_date IS NOT NULL AND exp.end_date <> ""
            WITH exp, apoc.date.parse(exp.end_date, 'ms', 'MMMM yyyy') AS parsed_end_date
            WHERE parsed_end_date < apoc.date.parse("January 2023", 'ms', 'MMMM yyyy')
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
        """
    },
    {
        "question": "What experiences has Arghya had after February 2022?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.start_date IS NOT NULL AND exp.start_date <> ""
            WITH exp, apoc.date.parse(exp.start_date, 'ms', 'MMMM yyyy') AS parsed_start_date
            WHERE parsed_start_date > apoc.date.parse("February 2022", 'ms', 'MMMM yyyy')
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
        """
    },
    {
        "question": "What experiences has Arghya had after 2022?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.start_date IS NOT NULL AND exp.start_date <> ""
            WITH exp, apoc.date.parse(exp.start_date, 'ms', 'MMMM yyyy') AS parsed_start_date
            WHERE parsed_start_date > apoc.date.parse("January 2022", 'ms', 'MMMM yyyy')
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
        """
    },
    {
        "question": "What experiences has Arghya had from February 2020 to November 2021?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.start_date IS NOT NULL AND exp.start_date <> ""
            WITH exp,
                 apoc.date.parse(exp.start_date, 'ms', 'MMMM yyyy') AS parsed_start_date,
                 CASE 
                     WHEN exp.end_date IS NULL OR exp.end_date = "" THEN timestamp()
                     ELSE apoc.date.parse(exp.end_date, 'ms', 'MMMM yyyy')
                 END AS parsed_end_date
            WHERE parsed_start_date >= apoc.date.parse("February 2020", 'ms', 'MMMM yyyy') AND
                  parsed_end_date <= apoc.date.parse("November 2021", 'ms', 'MMMM yyyy')
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
        """
    },
    {
        "question": "What experiences has Arghya had from 2020 to 2021?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.start_date IS NOT NULL AND exp.start_date <> ""
            WITH exp,
                 apoc.date.parse(exp.start_date, 'ms', 'MMMM yyyy') AS parsed_start_date,
                 CASE 
                     WHEN exp.end_date IS NULL OR exp.end_date = "" THEN timestamp()
                     ELSE apoc.date.parse(exp.end_date, 'ms', 'MMMM yyyy')
                 END AS parsed_end_date
            WHERE parsed_start_date >= apoc.date.parse("January 2020", 'ms', 'MMMM yyyy') AND
                  parsed_end_date <= apoc.date.parse("December 2021", 'ms', 'MMMM yyyy')
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
        """
    },
    {
        "question": "What experiences has Arghya had from February 2020 till date?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.start_date IS NOT NULL AND exp.start_date <> ""
            WITH exp,
                 apoc.date.parse(exp.start_date, 'ms', 'MMMM yyyy') AS parsed_start_date,
                 CASE 
                     WHEN exp.end_date IS NULL OR exp.end_date = "" THEN timestamp()
                     ELSE apoc.date.parse(exp.end_date, 'ms', 'MMMM yyyy')
                 END AS parsed_end_date
            WHERE parsed_start_date >= apoc.date.parse("February 2020", 'ms', 'MMMM yyyy') AND
                  parsed_end_date <= timestamp()
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
        """
    },
    {
        "question": "What experiences has Arghya had from 2020 till date?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience)
            WHERE exp.start_date IS NOT NULL AND exp.start_date <> ""
            WITH exp,
                 apoc.date.parse(exp.start_date, 'ms', 'MMMM yyyy') AS parsed_start_date,
                 CASE 
                     WHEN exp.end_date IS NULL OR exp.end_date = "" THEN timestamp()
                     ELSE apoc.date.parse(exp.end_date, 'ms', 'MMMM yyyy')
                 END AS parsed_end_date
            WHERE parsed_start_date >= apoc.date.parse("January 2020", 'ms', 'MMMM yyyy') AND
                  parsed_end_date <= timestamp()
            RETURN exp.title, exp.organisation_name, exp.start_date, exp.end_date
        """
    },
    {
        "question": "Compare Arghya's experience at Thoughtworks and CIIC Money Matters.",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp1:experience {{organisation_name: "Thoughtworks"}})
            MATCH (p)-[:HAS_EXPERIENCE]->(exp2:experience {{organisation_name: "CIIC Money Matters"}})
            RETURN exp1.title AS Thoughtworks_Experience, exp2.title AS CIIC_Experience, exp1.start_date, exp2.start_date
        """
    },
]

certificate = [
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
        "question": "Which certifications did Arghya achieve in 2022?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_CERTIFICATION]->(c:certifications) WHERE c.issue_date CONTAINS "2022" RETURN c.name, c.credential_url
        """
    },
    {
        "question": "Which certifications are the most recent for Arghya?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_CERTIFICATION]->(c:certifications)
            RETURN c.name, c.issue_date
            ORDER BY c.issue_date DESC
            LIMIT 3
        """
    },
]

skills = [
    {
        "question": "What skills did Arghya use at Thoughtworks?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_EXPERIENCE]->(exp:experience {{organisation_name: "Thoughtworks"}})
            MATCH (exp)-[:REQUIRED_SKILL]->(s:skills)
            RETURN s.name
        """
    },
    {
        "question": "What skills does Arghya have?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:IS_SKILLED]->(s:skills) RETURN s.name
        """
    },
]

language = [
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
]

blogs = [
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

honours_and_awards = [
    {
        "question": "What awards has Arghya received?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:RECEIVED_AWARD]->(h:honour_and_awards) RETURN h.title, h.associate_with, h.issue_date
        """
    },
    {
        "question": "What awards did Arghya receive after 2023?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:RECEIVED_AWARD]->(h:honour_and_awards)
            WHERE h.issue_date IS NOT NULL AND h.issue_date <> ""
            WITH h, apoc.date.parse(h.issue_date, 'ms', 'MMMM yyyy') AS parsed_date
            WHERE parsed_date > apoc.date.parse("January 2023", 'ms', 'MMMM yyyy')
            RETURN h.title, h.associate_with, h.issue_date
        """
    },
    {
        "question": "What awards did Arghya receive before 2023?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:RECEIVED_AWARD]->(h:honour_and_awards)
            WHERE h.issue_date IS NOT NULL AND h.issue_date <> ""
            WITH h, apoc.date.parse(h.issue_date, 'ms', 'MMMM yyyy') AS parsed_date
            WHERE parsed_date < apoc.date.parse("January 2023", 'ms', 'MMMM yyyy')
            RETURN h.title, h.associate_with, h.issue_date
        """
    },
    {
        "question": "What awards did Arghya receive in 2022?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:RECEIVED_AWARD]->(h:honour_and_awards)
            WHERE h.issue_date IS NOT NULL AND h.issue_date <> "" AND h.issue_date CONTAINS "2022"
            RETURN h.title, h.associate_with, h.issue_date
        """
    },
    {
        "question": "What awards did Arghya receive from 2021 to 2023?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:RECEIVED_AWARD]->(h:honour_and_awards)
            WHERE h.issue_date IS NOT NULL AND h.issue_date <> ""
            WITH h, apoc.date.parse(h.issue_date, 'ms', 'MMMM yyyy') AS parsed_date
            WHERE parsed_date >= apoc.date.parse("January 2021", 'ms', 'MMMM yyyy') AND
                  parsed_date <= apoc.date.parse("December 2023", 'ms', 'MMMM yyyy')
            RETURN h.title, h.associate_with, h.issue_date
        """
    }
]

recommendation = [
{
        "question": "Who recommended Arghya and what did they say?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_RECOMMENDATION]->(rec:recommendation) RETURN rec.recommender_name, rec.message
        """
    },
    {
        "question": "Has Arghya received any recommendation for teamwork?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_RECOMMENDATION]->(rec:recommendation) WHERE rec.message CONTAINS "teamwork" RETURN rec.recommender_name, rec.message
        """
    },
    {
        "question": "List all the positive recommendation Arghya received.",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:HAS_RECOMMENDATION]->(rec:recommendation)
            WHERE rec.sentiment = "positive"
            RETURN rec.recommender_name, rec.message
        """
    },
]

projects = [
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
    {
        "question": "How many projects has Arghya completed since 2020?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects)
            WHERE pr.date IS NOT NULL AND pr.date <> ""
            WITH pr, apoc.date.parse(pr.date, 'ms', 'MMMM yyyy') AS parsed_date
            WHERE parsed_date > apoc.date.parse("January 2020", 'ms', 'MMMM yyyy')
            RETURN COUNT(pr) AS Project_Count
        """
    },
    {
        "question": "What projects did Arghya work on that involved Java or Python?",
         "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects)-[:REQUIRED_SKILL]->(s:skills)
            WHERE s.name = "Java" OR s.name = "Python"
            RETURN pr.project_name, pr.description
        """
    },
    {
        "question": "What projects did Arghya work on before July 2022?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects)
            WHERE pr.date IS NOT NULL AND pr.date <> ""
            WITH pr, apoc.date.parse(pr.date, 'ms', 'MMMM yyyy') AS parsed_date
            WHERE parsed_date < apoc.date.parse("July 2022", 'ms', 'MMMM yyyy')
            RETURN pr.project_name, pr.date, pr.description
        """
    },
    {
        "question": "What projects did Arghya work on after July 2022?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects)
            WHERE pr.date IS NOT NULL AND pr.date <> ""
            WITH pr, apoc.date.parse(pr.date, 'ms', 'MMMM yyyy') AS parsed_date
            WHERE parsed_date > apoc.date.parse("July 2022", 'ms', 'MMMM yyyy')
            RETURN pr.project_name, pr.date, pr.description
        """
    },
    {
        "question": "What projects did Arghya work on from February 2022 to November 2023?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects)
            WHERE pr.date IS NOT NULL AND pr.date <> ""
            WITH pr, apoc.date.parse(pr.date, 'ms', 'MMMM yyyy') AS parsed_date
            WHERE parsed_date >= apoc.date.parse("February 2022", 'ms', 'MMMM yyyy') AND
                  parsed_date <= apoc.date.parse("November 2023", 'ms', 'MMMM yyyy')
            RETURN pr.project_name, pr.date, pr.description
        """
    },
    {
        "question": "What projects did Arghya work on from 2022 to 2023?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects)
            WHERE pr.date IS NOT NULL AND pr.date <> ""
            WITH pr, apoc.date.parse(pr.date, 'ms', 'MMMM yyyy') AS parsed_date
            WHERE parsed_date >= apoc.date.parse("January 2022", 'ms', 'MMMM yyyy') AND
                  parsed_date <= apoc.date.parse("December 2023", 'ms', 'MMMM yyyy')
            RETURN pr.project_name, pr.date, pr.description
        """
    },
    {
        "question": "What projects did Arghya work on from February 2022 till date?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects)
            WHERE pr.date IS NOT NULL AND pr.date <> ""
            WITH pr, apoc.date.parse(pr.date, 'ms', 'MMMM yyyy') AS parsed_date
            WHERE parsed_date >= apoc.date.parse("February 2022", 'ms', 'MMMM yyyy') AND
                  parsed_date <= timestamp()
            RETURN pr.project_name, pr.date, pr.description
        """
    },
    {
        "question": "What projects did Arghya work on from 2022 till date?",
        "query": """
            MATCH (p:person {{name: "Arghya Bandyopadhyay"}})-[:WORKED_ON_PROJECT]->(pr:projects)
            WHERE pr.date IS NOT NULL AND pr.date <> ""
            WITH pr, apoc.date.parse(pr.date, 'ms', 'MMMM yyyy') AS parsed_date
            WHERE parsed_date >= apoc.date.parse("January 2022", 'ms', 'MMMM yyyy') AND
                  parsed_date <= timestamp()
            RETURN pr.project_name, pr.date, pr.description
        """
    },
]