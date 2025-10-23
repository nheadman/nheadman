"""
Initialize and populate the diagnostic classification database.
Cross-references DSM-5-TR and ICD-11 diagnostic codes with criteria and descriptions.
"""

import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "diagnostic_database.db"


def create_database():
    """Create the database schema."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create DSM-5-TR table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dsm5_disorders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            diagnostic_criteria TEXT,
            specifiers TEXT,
            prevalence TEXT,
            differential_diagnosis TEXT
        )
    """)
    
    # Create ICD-11 table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS icd11_disorders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            diagnostic_requirements TEXT,
            exclusions TEXT,
            coding_notes TEXT
        )
    """)
    
    # Create cross-reference table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cross_references (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dsm5_code TEXT NOT NULL,
            icd11_code TEXT NOT NULL,
            relationship_type TEXT,
            notes TEXT,
            FOREIGN KEY (dsm5_code) REFERENCES dsm5_disorders(code),
            FOREIGN KEY (icd11_code) REFERENCES icd11_disorders(code)
        )
    """)
    
    # Create full-text search tables
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS dsm5_search USING fts5(
            code, name, category, description, diagnostic_criteria,
            content='dsm5_disorders', content_rowid='id'
        )
    """)
    
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS icd11_search USING fts5(
            code, name, category, description, diagnostic_requirements,
            content='icd11_disorders', content_rowid='id'
        )
    """)
    
    # Create triggers to keep FTS tables in sync
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS dsm5_ai AFTER INSERT ON dsm5_disorders BEGIN
            INSERT INTO dsm5_search(rowid, code, name, category, description, diagnostic_criteria)
            VALUES (new.id, new.code, new.name, new.category, new.description, new.diagnostic_criteria);
        END
    """)
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS dsm5_ad AFTER DELETE ON dsm5_disorders BEGIN
            DELETE FROM dsm5_search WHERE rowid = old.id;
        END
    """)
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS dsm5_au AFTER UPDATE ON dsm5_disorders BEGIN
            DELETE FROM dsm5_search WHERE rowid = old.id;
            INSERT INTO dsm5_search(rowid, code, name, category, description, diagnostic_criteria)
            VALUES (new.id, new.code, new.name, new.category, new.description, new.diagnostic_criteria);
        END
    """)
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS icd11_ai AFTER INSERT ON icd11_disorders BEGIN
            INSERT INTO icd11_search(rowid, code, name, category, description, diagnostic_requirements)
            VALUES (new.id, new.code, new.name, new.category, new.description, new.diagnostic_requirements);
        END
    """)
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS icd11_ad AFTER DELETE ON icd11_disorders BEGIN
            DELETE FROM icd11_search WHERE rowid = old.id;
        END
    """)
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS icd11_au AFTER UPDATE ON icd11_disorders BEGIN
            DELETE FROM icd11_search WHERE rowid = old.id;
            INSERT INTO icd11_search(rowid, code, name, category, description, diagnostic_requirements)
            VALUES (new.id, new.code, new.name, new.category, new.description, new.diagnostic_requirements);
        END
    """)
    
    conn.commit()
    conn.close()
    print(f"✓ Database schema created at {DATABASE_PATH}")


def populate_sample_data():
    """Populate the database with sample diagnostic data."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Sample DSM-5-TR disorders
    dsm5_data = [
        # Depressive Disorders
        (
            "296.21", "Major Depressive Disorder, Single Episode, Mild",
            "Depressive Disorders",
            "A mental disorder characterized by persistent sadness and loss of interest in activities, causing significant impairment in daily life.",
            """A. Five (or more) of the following symptoms have been present during the same 2-week period and represent a change from previous functioning; at least one symptom is either (1) depressed mood or (2) loss of interest or pleasure:
1. Depressed mood most of the day, nearly every day
2. Markedly diminished interest or pleasure in all, or almost all, activities
3. Significant weight loss when not dieting or weight gain
4. Insomnia or hypersomnia nearly every day
5. Psychomotor agitation or retardation nearly every day
6. Fatigue or loss of energy nearly every day
7. Feelings of worthlessness or excessive guilt
8. Diminished ability to think or concentrate
9. Recurrent thoughts of death or suicidal ideation

B. The symptoms cause clinically significant distress or impairment in social, occupational, or other important areas of functioning.

C. The episode is not attributable to the physiological effects of a substance or another medical condition.""",
            "With anxious distress, With mixed features, With melancholic features, With atypical features, With mood-congruent psychotic features, With mood-incongruent psychotic features, With catatonia, With peripartum onset, With seasonal pattern",
            "Lifetime prevalence: approximately 10-15% for males and 20-25% for females. 12-month prevalence: approximately 7%.",
            "Bipolar disorders, adjustment disorder with depressed mood, persistent depressive disorder, substance-induced depressive disorder, depressive disorder due to another medical condition"
        ),
        (
            "296.22", "Major Depressive Disorder, Single Episode, Moderate",
            "Depressive Disorders",
            "Major depressive disorder with moderate severity, characterized by symptoms between mild and severe.",
            "Same criteria as mild MDD (296.21), but with moderate symptom severity and functional impairment that is more than mild but less than severe.",
            "With anxious distress, With mixed features, With melancholic features, With atypical features, With mood-congruent psychotic features, With mood-incongruent psychotic features, With catatonia, With peripartum onset, With seasonal pattern",
            "Similar to mild MDD",
            "Same as mild MDD differential diagnosis"
        ),
        (
            "300.4", "Persistent Depressive Disorder (Dysthymia)",
            "Depressive Disorders",
            "Chronic form of depression lasting at least 2 years with depressed mood for most of the day, for more days than not.",
            """A. Depressed mood for most of the day, for more days than not, for at least 2 years.

B. Presence, while depressed, of two (or more) of the following:
1. Poor appetite or overeating
2. Insomnia or hypersomnia
3. Low energy or fatigue
4. Low self-esteem
5. Poor concentration or difficulty making decisions
6. Feelings of hopelessness

C. During the 2-year period, the individual has never been without the symptoms for more than 2 months at a time.

D. Criteria for a major depressive disorder may be continuously present for 2 years.

E. There has never been a manic episode or hypomanic episode.

F. The disturbance is not better explained by schizoaffective disorder, schizophrenia, or other psychotic disorders.

G. The symptoms are not attributable to the physiological effects of a substance or another medical condition.

H. The symptoms cause clinically significant distress or impairment.""",
            "With anxious distress, With atypical features, With melancholic features, With mood-congruent psychotic features, With mood-incongruent psychotic features, In partial remission, In full remission, Early onset, Late onset, With pure dysthymic syndrome, With persistent major depressive episode, With intermittent major depressive episodes",
            "Lifetime prevalence approximately 3-6%. More common in females.",
            "Major depressive disorder, bipolar disorders, cyclothymic disorder, adjustment disorder with depressed mood"
        ),
        # Anxiety Disorders
        (
            "300.01", "Panic Disorder",
            "Anxiety Disorders",
            "Characterized by recurrent unexpected panic attacks followed by at least one month of persistent concern about having additional attacks.",
            """A. Recurrent unexpected panic attacks. A panic attack is an abrupt surge of intense fear or discomfort that reaches a peak within minutes, with four (or more) of the following symptoms:
1. Palpitations, pounding heart, or accelerated heart rate
2. Sweating
3. Trembling or shaking
4. Sensations of shortness of breath or smothering
5. Feelings of choking
6. Chest pain or discomfort
7. Nausea or abdominal distress
8. Feeling dizzy, unsteady, light-headed, or faint
9. Chills or heat sensations
10. Paresthesias (numbness or tingling sensations)
11. Derealization or depersonalization
12. Fear of losing control or "going crazy"
13. Fear of dying

B. At least one of the attacks has been followed by 1 month (or more) of one or both:
1. Persistent concern or worry about additional panic attacks or their consequences
2. A significant maladaptive change in behavior related to the attacks

C. The disturbance is not attributable to the physiological effects of a substance or another medical condition.

D. The disturbance is not better explained by another mental disorder.""",
            "None",
            "2-3% of adults and adolescents in the United States annually. Females are more frequently affected than males at a rate of approximately 2:1.",
            "Substance-induced anxiety disorder, anxiety disorder due to another medical condition, other specified anxiety disorder, agoraphobia, social anxiety disorder, specific phobia, separation anxiety disorder"
        ),
        (
            "300.02", "Generalized Anxiety Disorder",
            "Anxiety Disorders",
            "Excessive anxiety and worry about various events or activities, occurring more days than not for at least 6 months.",
            """A. Excessive anxiety and worry (apprehensive expectation), occurring more days than not for at least 6 months, about a number of events or activities.

B. The individual finds it difficult to control the worry.

C. The anxiety and worry are associated with three (or more) of the following six symptoms (with at least some symptoms having been present for more days than not for the past 6 months):
1. Restlessness or feeling keyed up or on edge
2. Being easily fatigued
3. Difficulty concentrating or mind going blank
4. Irritability
5. Muscle tension
6. Sleep disturbance

D. The anxiety, worry, or physical symptoms cause clinically significant distress or impairment in social, occupational, or other important areas of functioning.

E. The disturbance is not attributable to the physiological effects of a substance or another medical condition.

F. The disturbance is not better explained by another mental disorder.""",
            "None",
            "Approximately 2.9% 12-month prevalence in the United States. Higher in females (2:1 ratio).",
            "Anxiety disorder due to another medical condition, substance-induced anxiety disorder, social anxiety disorder, obsessive-compulsive disorder, PTSD, adjustment disorder with anxiety, bipolar disorder, depressive disorders"
        ),
        (
            "300.23", "Social Anxiety Disorder (Social Phobia)",
            "Anxiety Disorders",
            "Marked fear or anxiety about social situations in which the individual is exposed to possible scrutiny by others.",
            """A. Marked fear or anxiety about one or more social situations in which the individual is exposed to possible scrutiny by others.

B. The individual fears that he or she will act in a way or show anxiety symptoms that will be negatively evaluated.

C. The social situations almost always provoke fear or anxiety.

D. The social situations are avoided or endured with intense fear or anxiety.

E. The fear or anxiety is out of proportion to the actual threat posed by the social situation.

F. The fear, anxiety, or avoidance is persistent, typically lasting for 6 months or more.

G. The fear, anxiety, or avoidance causes clinically significant distress or impairment.

H. The fear, anxiety, or avoidance is not attributable to the physiological effects of a substance or another medical condition.

I. The fear, anxiety, or avoidance is not better explained by another mental disorder.

J. If another medical condition is present, the fear, anxiety, or avoidance is clearly unrelated or is excessive.""",
            "Performance only (if the fear is restricted to speaking or performing in public)",
            "Approximately 7% 12-month prevalence in the United States. Lower in much of Asia, Africa, and Latin America (0.5-2.0%). Higher in females than males.",
            "Agoraphobia, panic disorder, separation anxiety disorder, autism spectrum disorder, body dysmorphic disorder, delusional disorder, major depressive disorder, avoidant personality disorder"
        ),
        # Trauma and Stressor-Related Disorders
        (
            "309.81", "Posttraumatic Stress Disorder",
            "Trauma- and Stressor-Related Disorders",
            "Development of characteristic symptoms following exposure to one or more traumatic events.",
            """A. Exposure to actual or threatened death, serious injury, or sexual violence in one (or more) of the following ways:
1. Directly experiencing the traumatic event(s)
2. Witnessing, in person, the event(s) as it occurred to others
3. Learning that the traumatic event(s) occurred to a close family member or close friend
4. Experiencing repeated or extreme exposure to aversive details of the traumatic event(s)

B. Presence of one (or more) intrusion symptoms associated with the traumatic event(s):
1. Recurrent, involuntary, and intrusive distressing memories
2. Recurrent distressing dreams
3. Dissociative reactions (e.g., flashbacks)
4. Intense or prolonged psychological distress at exposure to cues
5. Marked physiological reactions to cues

C. Persistent avoidance of stimuli associated with the traumatic event(s) (one or both):
1. Avoidance of distressing memories, thoughts, or feelings
2. Avoidance of external reminders

D. Negative alterations in cognitions and mood (two or more):
1. Inability to remember important aspects
2. Persistent negative beliefs or expectations
3. Persistent distorted cognitions about the cause or consequences
4. Persistent negative emotional state
5. Markedly diminished interest or participation in activities
6. Feelings of detachment or estrangement from others
7. Persistent inability to experience positive emotions

E. Marked alterations in arousal and reactivity (two or more):
1. Irritable behavior and angry outbursts
2. Reckless or self-destructive behavior
3. Hypervigilance
4. Exaggerated startle response
5. Problems with concentration
6. Sleep disturbance

F. Duration of the disturbance is more than 1 month.

G. The disturbance causes clinically significant distress or impairment.

H. The disturbance is not attributable to the physiological effects of a substance or medical condition.""",
            "With dissociative symptoms (depersonalization or derealization), With delayed expression (full diagnostic criteria not met until at least 6 months after the event)",
            "In the United States, projected lifetime risk by age 75 years is 8.7%. 12-month prevalence is about 3.5% in U.S. adults. Higher in females and certain occupational groups.",
            "Adjustment disorders, acute stress disorder, other anxiety disorders, obsessive-compulsive disorder, major depressive disorder, personality disorders, dissociative disorders, traumatic brain injury"
        ),
        (
            "309.0", "Adjustment Disorder",
            "Trauma- and Stressor-Related Disorders",
            "Development of emotional or behavioral symptoms in response to an identifiable stressor occurring within 3 months of the onset of the stressor.",
            """A. The development of emotional or behavioral symptoms in response to an identifiable stressor(s) occurring within 3 months of the onset of the stressor(s).

B. These symptoms or behaviors are clinically significant, as evidenced by one or both:
1. Marked distress that is out of proportion to the severity or intensity of the stressor
2. Significant impairment in social, occupational, or other important areas of functioning

C. The stress-related disturbance does not meet the criteria for another mental disorder and is not merely an exacerbation of a preexisting mental disorder.

D. The symptoms do not represent normal bereavement.

E. Once the stressor or its consequences have terminated, the symptoms do not persist for more than an additional 6 months.""",
            "With depressed mood, With anxiety, With mixed anxiety and depressed mood, With disturbance of conduct, With mixed disturbance of emotions and conduct, Unspecified. Specify whether: Acute (duration less than 6 months), Persistent/Chronic (duration 6 months or more)",
            "Very common, particularly in response to major life stressors. Prevalence varies based on population and type of stressor.",
            "Major depressive disorder, PTSD, acute stress disorder, anxiety disorders, personality disorders, psychological factors affecting other medical conditions, normal stress reactions"
        ),
        # Obsessive-Compulsive and Related Disorders
        (
            "300.3", "Obsessive-Compulsive Disorder",
            "Obsessive-Compulsive and Related Disorders",
            "Presence of obsessions, compulsions, or both that are time-consuming or cause clinically significant distress or impairment.",
            """A. Presence of obsessions, compulsions, or both:

Obsessions are defined by (1) and (2):
1. Recurrent and persistent thoughts, urges, or images that are experienced as intrusive and unwanted
2. The individual attempts to ignore or suppress such thoughts, urges, or images, or to neutralize them with some other thought or action

Compulsions are defined by (1) and (2):
1. Repetitive behaviors or mental acts that the individual feels driven to perform in response to an obsession or according to rules
2. The behaviors or mental acts are aimed at preventing or reducing anxiety or distress

B. The obsessions or compulsions are time-consuming (e.g., take more than 1 hour per day) or cause clinically significant distress or impairment.

C. The obsessive-compulsive symptoms are not attributable to the physiological effects of a substance or another medical condition.

D. The disturbance is not better explained by the symptoms of another mental disorder.""",
            "With good or fair insight, With poor insight, With absent insight/delusional beliefs. Specify if: Tic-related",
            "12-month prevalence approximately 1.2% in the United States. Females affected at slightly higher rate in adulthood. Males more commonly affected in childhood.",
            "Body dysmorphic disorder, hoarding disorder, trichotillomania, excoriation disorder, substance-induced obsessive-compulsive disorder, obsessive-compulsive personality disorder, anxiety disorders, major depressive disorder, other obsessive-compulsive and related disorders, schizophrenia spectrum disorders"
        ),
        # Attention-Deficit/Hyperactivity Disorder
        (
            "314.01", "Attention-Deficit/Hyperactivity Disorder, Combined Presentation",
            "Neurodevelopmental Disorders",
            "A persistent pattern of inattention and/or hyperactivity-impulsivity that interferes with functioning or development.",
            """A. A persistent pattern of inattention and/or hyperactivity-impulsivity that interferes with functioning or development, as characterized by (1) and/or (2):

1. INATTENTION: Six (or more) of the following symptoms have persisted for at least 6 months to a degree that is inconsistent with developmental level:
a. Often fails to give close attention to details or makes careless mistakes
b. Often has difficulty sustaining attention in tasks or play activities
c. Often does not seem to listen when spoken to directly
d. Often does not follow through on instructions and fails to finish schoolwork/work
e. Often has difficulty organizing tasks and activities
f. Often avoids, dislikes, or is reluctant to engage in tasks requiring sustained mental effort
g. Often loses things necessary for tasks or activities
h. Is often easily distracted by extraneous stimuli
i. Is often forgetful in daily activities

2. HYPERACTIVITY AND IMPULSIVITY: Six (or more) of the following symptoms have persisted for at least 6 months:
a. Often fidgets with or taps hands or feet or squirms in seat
b. Often leaves seat in situations when remaining seated is expected
c. Often runs about or climbs in situations where it is inappropriate
d. Often unable to play or engage in leisure activities quietly
e. Is often "on the go" acting as if "driven by a motor"
f. Often talks excessively
g. Often blurts out an answer before a question has been completed
h. Often has difficulty waiting his or her turn
i. Often interrupts or intrudes on others

B. Several inattentive or hyperactive-impulsive symptoms were present prior to age 12 years.

C. Several inattentive or hyperactive-impulsive symptoms are present in two or more settings.

D. Clear evidence that the symptoms interfere with, or reduce the quality of, social, academic, or occupational functioning.

E. The symptoms do not occur exclusively during the course of schizophrenia or another psychotic disorder and are not better explained by another mental disorder.""",
            "In partial remission. Specify current severity: Mild, Moderate, Severe",
            "Approximately 5% of children and 2.5% of adults. More frequent in males than females (2:1 ratio in children).",
            "Oppositional defiant disorder, intermittent explosive disorder, other neurodevelopmental disorders, specific learning disorder, autism spectrum disorder, anxiety disorders, depressive disorders, bipolar disorder, disruptive mood dysregulation disorder, substance use disorders, personality disorders, psychotic disorders, medication-induced symptoms"
        ),
        # Bipolar Disorders
        (
            "296.41", "Bipolar I Disorder, Most Recent Episode Manic, Mild",
            "Bipolar and Related Disorders",
            "A distinct period of abnormally and persistently elevated, expansive, or irritable mood and abnormally increased activity or energy.",
            """For a diagnosis of bipolar I disorder, it is necessary to meet the following criteria for a manic episode. The manic episode may have been preceded by and may be followed by hypomanic or major depressive episodes.

MANIC EPISODE:
A. A distinct period of abnormally and persistently elevated, expansive, or irritable mood and abnormally and persistently increased goal-directed activity or energy, lasting at least 1 week and present most of the day, nearly every day.

B. During the period of mood disturbance and increased energy or activity, three (or more) of the following symptoms have persisted (four if the mood is only irritable):
1. Inflated self-esteem or grandiosity
2. Decreased need for sleep
3. More talkative than usual or pressure to keep talking
4. Flight of ideas or subjective experience that thoughts are racing
5. Distractibility
6. Increase in goal-directed activity or psychomotor agitation
7. Excessive involvement in activities that have a high potential for painful consequences

C. The mood disturbance is sufficiently severe to cause marked impairment in social or occupational functioning or to necessitate hospitalization to prevent harm to self or others, or there are psychotic features.

D. The episode is not attributable to the physiological effects of a substance or another medical condition.""",
            "With anxious distress, With mixed features, With rapid cycling, With melancholic features, With atypical features, With mood-congruent psychotic features, With mood-incongruent psychotic features, With catatonia, With peripartum onset, With seasonal pattern",
            "12-month prevalence estimate of bipolar I disorder is approximately 0.6% internationally. Lifetime prevalence in the United States is approximately 1.0%.",
            "Bipolar II disorder, major depressive disorder, cyclothymic disorder, substance/medication-induced bipolar disorder, bipolar disorder due to another medical condition, ADHD, personality disorders, schizophrenia spectrum disorders"
        ),
        (
            "296.89", "Bipolar II Disorder",
            "Bipolar and Related Disorders",
            "Characterized by a clinical course of recurring mood episodes consisting of one or more major depressive episodes and at least one hypomanic episode.",
            """A. Criteria have been met for at least one hypomanic episode and at least one major depressive episode.

B. There has never been a manic episode.

C. The occurrence of the hypomanic episode(s) and major depressive episode(s) is not better explained by schizoaffective disorder, schizophrenia, or other psychotic disorders.

D. The symptoms of depression or the unpredictability caused by frequent alternation between periods of depression and hypomania causes clinically significant distress or impairment.

HYPOMANIC EPISODE:
A. A distinct period of abnormally and persistently elevated, expansive, or irritable mood and abnormally and persistently increased activity or energy, lasting at least 4 consecutive days.

B. During the period of mood disturbance and increased energy and activity, three (or more) of the following symptoms have persisted:
1. Inflated self-esteem or grandiosity
2. Decreased need for sleep
3. More talkative than usual
4. Flight of ideas or racing thoughts
5. Distractibility
6. Increase in goal-directed activity or psychomotor agitation
7. Excessive involvement in activities with high potential for painful consequences

C. The episode is associated with an unequivocal change in functioning that is uncharacteristic of the individual.

D. The disturbance in mood and the change in functioning are observable by others.

E. The episode is not severe enough to cause marked impairment or to necessitate hospitalization.

F. The episode is not attributable to the physiological effects of a substance.""",
            "With anxious distress, With mixed features, With rapid cycling, With mood-congruent psychotic features, With mood-incongruent psychotic features, With catatonia, With peripartum onset, With seasonal pattern, In partial remission, In full remission. Specify current severity",
            "12-month prevalence of bipolar II disorder internationally is approximately 0.3%. Lifetime prevalence in the United States is approximately 0.8%.",
            "Major depressive disorder, cyclothymic disorder, bipolar I disorder, substance/medication-induced bipolar disorder, ADHD, personality disorders, schizophrenia spectrum disorders"
        ),
        # Schizophrenia Spectrum
        (
            "295.90", "Schizophrenia",
            "Schizophrenia Spectrum and Other Psychotic Disorders",
            "A chronic mental disorder characterized by distortions in thinking, perception, emotions, language, sense of self and behavior.",
            """A. Two (or more) of the following, each present for a significant portion of time during a 1-month period (or less if successfully treated). At least one of these must be (1), (2), or (3):
1. Delusions
2. Hallucinations
3. Disorganized speech
4. Grossly disorganized or catatonic behavior
5. Negative symptoms (diminished emotional expression or avolition)

B. For a significant portion of the time since the onset of the disturbance, level of functioning in one or more major areas is markedly below the level achieved prior to the onset.

C. Continuous signs of the disturbance persist for at least 6 months. This 6-month period must include at least 1 month of symptoms that meet Criterion A (active-phase symptoms) and may include periods of prodromal or residual symptoms.

D. Schizoaffective disorder and depressive or bipolar disorder with psychotic features have been ruled out.

E. The disturbance is not attributable to the physiological effects of a substance or another medical condition.

F. If there is a history of autism spectrum disorder or a communication disorder of childhood onset, the additional diagnosis of schizophrenia is made only if prominent delusions or hallucinations are present for at least 1 month.""",
            "First episode, Multiple episodes, Continuous, Unspecified. With catatonia. Specify current severity",
            "Lifetime prevalence approximately 0.3%-0.7%. Median lifetime morbid risk is approximately 7 per 1,000 persons.",
            "Schizoaffective disorder, bipolar and depressive disorders with psychotic features, schizophreniform disorder, brief psychotic disorder, delusional disorder, substance/medication-induced psychotic disorder, psychotic disorder due to another medical condition, autism spectrum disorder, personality disorders"
        ),
    ]
    
    # Insert DSM-5-TR data
    cursor.executemany("""
        INSERT OR IGNORE INTO dsm5_disorders 
        (code, name, category, description, diagnostic_criteria, specifiers, prevalence, differential_diagnosis)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, dsm5_data)
    
    # Sample ICD-11 disorders
    icd11_data = [
        # Mood Disorders
        (
            "6A70", "Single episode depressive disorder",
            "Mood disorders",
            "Single episode depressive disorder is characterized by the presence or history of one depressive episode when there is no history of prior depressive episodes. A depressive episode is characterized by a period of depressed mood or diminished interest in activities occurring most of the day, nearly every day during a period lasting at least two weeks accompanied by other symptoms such as difficulty concentrating, feelings of worthlessness or excessive or inappropriate guilt, hopelessness, recurrent thoughts of death or suicide, changes in appetite or sleep, psychomotor agitation or retardation, and reduced energy or fatigue.",
            "Requires depressed mood or diminished interest in activities for at least 2 weeks, plus additional symptoms causing significant impairment. Must be the first episode with no history of prior depressive or manic/hypomanic episodes.",
            "Manic, mixed or hypomanic episode rules out this diagnosis (consider bipolar disorder instead). Exclude substance-induced mood disorder, mood disorder due to a medical condition.",
            "Severity is coded with additional character: 0=currently asymptomatic, 1=mild, 2=moderate without psychotic symptoms, 3=moderate with psychotic symptoms, 4=severe without psychotic symptoms, 5=severe with psychotic symptoms"
        ),
        (
            "6A71", "Recurrent depressive disorder",
            "Mood disorders",
            "Recurrent depressive disorder is characterized by a history of at least two depressive episodes separated by at least several months without significant mood disturbance. A depressive episode is characterized by a period of depressed mood or diminished interest in activities occurring most of the day, nearly every day during a period lasting at least two weeks accompanied by other symptoms.",
            "Requires at least 2 separate depressive episodes with symptom-free periods in between. Each episode must meet criteria for depressive episode with significant impairment.",
            "Exclude bipolar disorder (presence of manic/hypomanic episodes), persistent mood disorders, substance-induced mood disorder, mood disorder due to medical condition.",
            "Current episode severity coded with additional character. Can specify with prominent anxiety symptoms, with panic attacks, with seasonal pattern."
        ),
        (
            "6A73", "Dysthymic disorder",
            "Mood disorders",
            "Dysthymic disorder is characterized by a persistent depressed mood (most of the day, more days than not) lasting for at least 2 years, accompanied by additional depressive symptoms that do not meet the diagnostic requirements for a depressive episode.",
            "Persistent depressed mood for at least 2 years with some additional depressive symptoms present, but not meeting full criteria for depressive episode. Never without symptoms for more than 2 months at a time during the 2-year period.",
            "If full criteria for depressive episode are met for extended period, diagnose depressive disorder instead. Exclude substance-induced mood disorder, mood disorder due to medical condition.",
            "Similar to DSM-5 Persistent Depressive Disorder. Can have superimposed depressive episodes."
        ),
        # Anxiety and Fear-Related Disorders
        (
            "6B01", "Panic disorder",
            "Anxiety and fear-related disorders",
            "Panic disorder is characterized by recurrent unexpected panic attacks that are not restricted to particular stimuli or situations. Panic attacks are discrete episodes of intense fear or apprehension accompanied by the rapid and concurrent onset of characteristic symptoms (e.g., palpitations, chest pain, dizziness, shortness of breath).",
            "Requires recurrent unexpected panic attacks (at least several) with at least 1 month of persistent concern about panic attacks or maladaptive behavioral changes due to panic attacks. Panic attacks must have rapid onset of intense fear with multiple characteristic somatic and cognitive symptoms.",
            "Exclude panic attacks occurring exclusively in response to specific feared stimuli (see specific phobia, social anxiety), due to substances, or due to medical conditions. Exclude if panic is part of other mental disorders.",
            "Often co-occurs with agoraphobia (code separately if present). Disability depends on severity and associated avoidance."
        ),
        (
            "6B02", "Agoraphobia",
            "Anxiety and fear-related disorders",
            "Agoraphobia is characterized by marked and excessive fear or anxiety about multiple situations where escape might be difficult or help might not be available, such as using public transportation, being in crowds, being outside of the home alone.",
            "Marked fear or anxiety about at least 2 of: public transportation, open spaces, enclosed spaces, crowds, or being outside home alone. Fear is about difficulty escaping or getting help if panic-like symptoms occur. Situations actively avoided or require companion.",
            "Fear must be out of proportion to actual danger. Exclude specific phobia (fear limited to one situation), social anxiety disorder, separation anxiety, PTSD. Exclude substance-induced or due to medical condition.",
            "Typically chronic unless treated. Can occur with or without panic disorder."
        ),
        (
            "6B03", "Specific phobia",
            "Anxiety and fear-related disorders",
            "Specific phobia is characterized by marked and excessive fear or anxiety that consistently occurs when exposed to one or more specific objects or situations and that is out of proportion to actual danger.",
            "Marked fear or anxiety consistently triggered by specific object or situation (e.g., animals, heights, blood, flying). Fear is out of proportion to actual danger. Object/situation actively avoided or endured with intense fear. Symptoms present for several months.",
            "Fear must be focused and circumscribed. Exclude agoraphobia, social anxiety disorder, separation anxiety, obsessive-compulsive disorder, PTSD.",
            "Specify type: animal, natural environment, blood-injection-injury, situational, or other. Usually begins in childhood."
        ),
        (
            "6B04", "Social anxiety disorder",
            "Anxiety and fear-related disorders",
            "Social anxiety disorder is characterized by marked and excessive fear or anxiety that consistently occurs in social situations in which the individual may be evaluated by others. The individual is concerned that he or she will act in a way, or show anxiety symptoms, that will be negatively evaluated by others.",
            "Marked fear or anxiety in social situations where scrutiny by others is possible. Fear of showing anxiety symptoms or acting in ways that will be negatively evaluated. Social situations consistently provoke fear and are avoided or endured with intense fear.",
            "Fear must be out of proportion to actual threat. Exclude agoraphobia, separation anxiety disorder, disorders on autism spectrum, body dysmorphic disorder, olfactory reference disorder.",
            "Typically begins in adolescence. Can be generalized (most social situations) or performance-only type."
        ),
        (
            "6B05", "Separation anxiety disorder",
            "Anxiety and fear-related disorders",
            "Separation anxiety disorder is characterized by marked and excessive fear or anxiety about separation from specific attachment figures. In children, the fear is typically focused on caregivers. Symptoms may include worry about harm or loss of attachment figures, reluctance to go out, nightmares, and physical complaints.",
            "Excessive fear or anxiety about separation from major attachment figures, beyond what is expected for developmental level. Symptoms include worry about harm to attachment figures, reluctance to go away from home, fear of being alone, nightmares, physical complaints. Duration at least several months.",
            "Consider developmental norms. Exclude agoraphobia, social anxiety disorder, panic disorder, generalized anxiety disorder, PTSD, psychotic disorders.",
            "Can occur in children, adolescents, or adults. In adults, focus is often on partner or children."
        ),
        (
            "6B06", "Selective mutism",
            "Anxiety and fear-related disorders",
            "Selective mutism is characterized by consistent selectivity in speaking such that a child demonstrates adequate language competence in specific social situations, typically at home, but consistently fails to speak in others, typically at school.",
            "Consistent failure to speak in specific social situations where speaking is expected (e.g., school) despite speaking in other situations (e.g., at home). Duration at least 1 month. Language ability is adequate. Interferes with educational achievement or social communication.",
            "Exclude communication disorders, autism spectrum disorder, schizophrenia spectrum disorders. Not due to lack of knowledge of or comfort with spoken language.",
            "Typically identified when child starts school. Often associated with social anxiety."
        ),
        (
            "6B00", "Generalised anxiety disorder",
            "Anxiety and fear-related disorders",
            "Generalised anxiety disorder is characterized by marked symptoms of anxiety that persist for at least several months, manifested by either general apprehensiveness or excessive worry focused on multiple everyday events, most often concerning family, health, finances, and school or work.",
            "Marked and excessive anxiety or worry about multiple events or activities, present for at least several months. Anxiety is generalized and not restricted to particular circumstances. Accompanied by symptoms such as restlessness, muscle tension, difficulty concentrating, irritability, sleep disturbance.",
            "Anxiety is not better accounted for by other anxiety disorders. Exclude substance-induced anxiety, anxiety due to medical condition, psychotic disorders, mood disorders.",
            "One of the most common anxiety disorders. Chronic fluctuating course typical."
        ),
        # Disorders specifically associated with stress
        (
            "6B40", "Post-traumatic stress disorder",
            "Disorders specifically associated with stress",
            "Post-traumatic stress disorder develops following exposure to an extremely threatening or horrific event or series of events. It is characterized by: re-experiencing the traumatic event(s), avoidance of thoughts and memories or external reminders, and persistent perceptions of heightened current threat.",
            "Exposure to extremely threatening or horrific event. Core features: 1) Re-experiencing in present (vivid intrusive memories, flashbacks, nightmares); 2) Avoidance of thoughts/memories or external reminders; 3) Persistent perception of heightened threat (hypervigilance, startle). Symptoms persist at least several weeks and cause significant impairment.",
            "Symptoms must develop following trauma. Exclude adjustment disorder (less severe symptoms), acute stress reaction (symptoms within first month), complex PTSD (has additional features). Exclude substance-induced symptoms.",
            "Can specify if symptoms present 6+ months after trauma (delayed onset). More severe form: Complex PTSD (6B41) includes additional problems with affect regulation, self-concept, relationships."
        ),
        (
            "6B41", "Complex post-traumatic stress disorder",
            "Disorders specifically associated with stress",
            "Complex post-traumatic stress disorder develops following exposure to an event or series of events of an extremely threatening or horrific nature, most commonly prolonged or repetitive events. It includes all PTSD symptoms plus severe and persistent problems in affect regulation, negative self-concept, and disturbances in relationships.",
            "All requirements for PTSD plus: 1) Severe problems with affect regulation; 2) Persistent negative beliefs about self as diminished, defeated, or worthless with shame, guilt, or failure; 3) Persistent difficulties in sustaining relationships and in feeling close to others. Symptoms cause significant impairment.",
            "Requires trauma exposure. Distinguished from PTSD by additional symptoms. Exclude personality disorders, mood disorders, dissociative disorders unless they co-occur.",
            "Typically results from prolonged trauma (e.g., childhood abuse, torture, prolonged domestic violence). More severe and complex than PTSD."
        ),
        (
            "6B42", "Prolonged grief disorder",
            "Disorders specifically associated with stress",
            "Prolonged grief disorder is characterized by a persistent and pervasive longing for, or persistent preoccupation with, the deceased that lasts beyond 6 months after the death. The grief response persists for an atypically long period following the loss and is of such intensity that it impairs functioning.",
            "Persistent and pervasive grief response after death of partner, parent, child or other close person. Includes intense longing for deceased or preoccupation with deceased. Accompanied by intense emotional pain, difficulty accepting death, feeling life is meaningless, identity confusion, difficulty engaging with social/other activities. Duration: symptoms persist beyond expected cultural, social, religious norms (at least 6 months).",
            "Differentiate from non-pathological bereavement. Exclude depressive disorder, PTSD, adjustment disorder unless they co-occur. Not due to cultural, social, or religious practices.",
            "Previously called complicated grief or persistent complex bereavement disorder. New to ICD-11."
        ),
        (
            "6B43", "Adjustment disorder",
            "Disorders specifically associated with stress",
            "Adjustment disorder is a maladaptive reaction to an identifiable psychosocial stressor or multiple stressors that usually emerges within a month of the stressor. Characterized by preoccupation with the stressor or its consequences and failure to adapt accompanied by various emotional symptoms.",
            "Occurs in response to identifiable stressor(s), usually within 1 month. Characterized by: 1) Preoccupation with stressor or its consequences; 2) Failure to adapt associated with symptoms such as depressed mood, anxiety, worry, feeling unable to cope, interference with daily activities. Duration typically does not exceed 6 months unless stressor persists.",
            "Symptoms are in excess of expected reaction but less severe than other disorders. Exclude normal stress reactions, mood disorders, anxiety disorders, PTSD, prolonged grief disorder. Symptoms resolve when stressor/consequences end.",
            "Can specify predominant symptoms: with depressed mood, with anxiety, with disturbance of conduct, with mixed disturbance of emotions and conduct."
        ),
        # Obsessive-compulsive and related disorders
        (
            "6B20", "Obsessive-compulsive disorder",
            "Obsessive-compulsive or related disorders",
            "Obsessive-compulsive disorder is characterized by the presence of persistent obsessions or compulsions, or most commonly both. Obsessions are repetitive and persistent thoughts, images or impulses that are intrusive, unwanted, and commonly associated with anxiety. Compulsions are repetitive behaviours or mental acts that an individual feels compelled to perform in response to an obsession.",
            "Presence of obsessions (intrusive unwanted thoughts, images, impulses causing distress) and/or compulsions (repetitive behaviors or mental acts performed to reduce distress or prevent feared events). Obsessions/compulsions are time-consuming (more than 1 hour/day) or cause significant distress/impairment. Individual recognizes obsessions/compulsions as own thoughts/behaviors.",
            "Exclude body dysmorphic disorder, olfactory reference disorder, hypochondriasis, hoarding disorder if symptoms restricted to those concerns. Exclude OCD symptoms occurring exclusively during psychotic disorder or mood episode.",
            "Can specify with: good/fair insight, poor insight, absent insight (delusional beliefs). Wide range of content themes."
        ),
        (
            "6B21", "Body dysmorphic disorder",
            "Obsessive-compulsive or related disorders",
            "Body dysmorphic disorder is characterized by persistent preoccupation with one or more perceived defects or flaws in appearance that are either not observable or appear only slight to others.",
            "Persistent preoccupation with perceived defect(s) in physical appearance that are not observable or appear slight to others. Preoccupation causes significant distress or impairment. Leads to repetitive behaviors (mirror checking, excessive grooming, skin picking, reassurance seeking) or mental acts. Preoccupation not better explained by weight/body fat concerns in eating disorder.",
            "Differentiate from normal appearance concerns. Exclude concerns limited to weight/body fat (see eating disorders), olfactory reference disorder, illness anxiety disorder, delusional disorder somatic type, avoidant personality disorder.",
            "Can specify if with muscle dysmorphia (preoccupation that body build is too small/insufficiently muscular). High rates of depression and suicide."
        ),
        (
            "6B22", "Olfactory reference disorder",
            "Obsessive-compulsive or related disorders",
            "Olfactory reference disorder is characterized by persistent preoccupation with the belief that one emits a foul or offensive body odor or breath that is either not observable or appears only slight to others.",
            "Persistent preoccupation with belief that one emits foul or offensive odor (body odor, breath, flatulence, genital smell) that is not observable or appears slight to others. Leads to repetitive behaviors (checking for smell, excessive washing, perfume use, reassurance seeking) or mental acts. Causes significant distress or impairment.",
            "Exclude body dysmorphic disorder (appearance focus), OCD (if part of contamination obsessions), social anxiety disorder without belief about body odor, delusional disorder if belief held with delusional intensity, psychotic disorders.",
            "Culturally sensitive assessment needed. Can have varying levels of insight. Often leads to social avoidance."
        ),
        (
            "6B24", "Hoarding disorder",
            "Obsessive-compulsive or related disorders",
            "Hoarding disorder is characterized by accumulation of possessions due to excessive acquisition of or difficulty discarding possessions, regardless of their actual value. Excessive acquisition is characterized by repetitive urges or behaviours related to amassing or buying items. Difficulty discarding possessions is characterized by a perceived need to save items and distress associated with discarding them.",
            "Accumulation of possessions that congest and clutter living areas to extent that use is substantially compromised. Accumulation due to: 1) Difficulty discarding possessions due to perceived need to save items and distress when discarding, and/or 2) Excessive acquisition. Results in significant distress or impairment in functioning.",
            "Exclude normative collecting, accumulation due to other medical conditions (dementia), accumulation resulting from inadequate living conditions, symptoms of other mental disorders (delusions in psychotic disorder, loss of energy in depression, decreased need for possessions in autism).",
            "Insight often poor. Creates fire hazards and health risks. Often egosyntonic."
        ),
        # Attention deficit hyperactivity disorder
        (
            "6A05", "Attention deficit hyperactivity disorder",
            "Neurodevelopmental disorders",
            "Attention deficit hyperactivity disorder is characterized by a persistent pattern of inattention and/or hyperactivity-impulsivity that has a direct negative impact on academic, occupational or social functioning.",
            "Persistent pattern (at least 6 months) of inattention and/or hyperactivity-impulsivity with direct negative impact on academic, occupational, or social functioning. Several symptoms present before age 12. Symptoms present across situations (though may vary by context). Not better explained by another mental disorder.",
            "Exclude if symptoms occur exclusively during course of schizophrenia spectrum disorders, other psychotic disorders, mood disorders, anxiety disorders, dissociative disorders, personality disorders, substance intoxication/withdrawal. Consider developmental disorders, specific learning disorders.",
            "Can specify presentation: predominantly inattentive, predominantly hyperactive-impulsive, or combined. Severity: mild, moderate, severe. Often persists into adulthood with changing symptom profile."
        ),
        # Bipolar disorders
        (
            "6A60", "Bipolar type I disorder",
            "Bipolar or related disorders",
            "Bipolar type I disorder is characterized by the occurrence of one or more manic or mixed episodes. A manic episode is an extreme mood state characterized by euphoria, irritability, or expansiveness, with several typical symptoms accompanied by significant impairment in functioning.",
            "At least one manic episode (period of abnormally elevated, expansive, or irritable mood plus increased activity/energy lasting at least 1 week unless hospitalization required). During mood disturbance, several symptoms present: increased self-esteem/grandiosity, decreased sleep need, talkativeness, racing thoughts, distractibility, increased goal-directed activity, excessive risk-taking. Causes marked impairment.",
            "Exclude substance-induced mania, secondary mania due to medical condition, schizophrenia and other psychotic disorders. If manic symptoms only occur during antidepressant treatment, do not diagnose bipolar disorder.",
            "Specify current episode: manic, depressive, mixed, or in remission. Lifetime diagnosis even if currently in remission. High recurrence risk."
        ),
        (
            "6A61", "Bipolar type II disorder",
            "Bipolar or related disorders",
            "Bipolar type II disorder is characterized by the occurrence of one or more hypomanic episodes and at least one depressive episode. There is no history of manic or mixed episodes.",
            "At least one hypomanic episode (period of abnormally elevated, expansive, or irritable mood lasting at least several days, less severe than mania, does not cause marked impairment) AND at least one depressive episode. No history of manic or mixed episodes.",
            "Exclude bipolar type I disorder (manic episodes present), cyclothymic disorder (no full depressive episodes), recurrent depressive disorder (no hypomanic episodes), substance-induced mood disorder, secondary mood disorder.",
            "Specify current episode: hypomanic, depressive, mixed, or in remission. Depressive episodes often predominate. Risk of progression to bipolar I disorder is low."
        ),
        (
            "6A62", "Cyclothymic disorder",
            "Bipolar or related disorders",
            "Cyclothymic disorder is characterized by persistent mood instability over an extended period of time characterized by numerous periods of hypomanic and depressive symptoms. The symptoms are present for most of the time, but no individual episode meets the diagnostic requirements for a Hypomanic Episode or a Depressive Episode.",
            "Persistent mood instability over at least 2 years with numerous periods of hypomanic symptoms and depressive symptoms. Symptoms present most of the time, but no individual episode meets full criteria for hypomanic or depressive episode. Never without symptoms for more than 2 months at a time. Causes significant distress or impairment.",
            "If full hypomanic or depressive episode develops, change diagnosis to bipolar disorder. Exclude substance-induced mood disorder, personality disorders (particularly borderline personality disorder).",
            "Chronic fluctuating course. May evolve into bipolar I or II disorder. Interpersonal and occupational difficulties common."
        ),
        # Schizophrenia spectrum
        (
            "6A20", "Schizophrenia",
            "Schizophrenia or other primary psychotic disorders",
            "Schizophrenia is characterized by disturbances in multiple mental modalities, including thinking, perception, self-experience, cognition, volition, affect, and behaviour. Symptoms include persistent delusions, persistent hallucinations, disorganized thinking, grossly disorganized behaviour, and experiences of passivity and control.",
            "Presence of at least two of: 1) Persistent delusions; 2) Persistent hallucinations; 3) Disorganized thinking (formal thought disorder); 4) Experiences of influence, passivity, or control; 5) Negative symptoms; 6) Grossly disorganized behaviour. Symptoms present for at least 1 month. Significant impairment in functioning. Not attributable to substance or medical condition.",
            "Exclude schizoaffective disorder (prominent mood episodes), mood disorders with psychotic symptoms, brief psychotic disorders, acute and transient psychotic disorders, delusional disorder, substance-induced psychotic disorder, secondary psychotic disorders.",
            "Specify first episode vs. multiple episodes, currently symptomatic vs. in remission. Can code predominant symptom pattern. Cognitive impairment common."
        ),
    ]
    
    # Insert ICD-11 data
    cursor.executemany("""
        INSERT OR IGNORE INTO icd11_disorders 
        (code, name, category, description, diagnostic_requirements, exclusions, coding_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, icd11_data)
    
    # Cross-references between DSM-5-TR and ICD-11
    cross_refs = [
        ("296.21", "6A70", "equivalent", "Major Depressive Disorder, Single Episode maps to Single episode depressive disorder"),
        ("296.22", "6A70", "equivalent", "MDD Moderate severity also maps to 6A70 with severity specified"),
        ("300.4", "6A73", "equivalent", "Persistent Depressive Disorder corresponds to Dysthymic disorder"),
        ("296.21", "6A71", "related", "If there are recurrent episodes, the ICD-11 code becomes 6A71"),
        ("296.22", "6A71", "related", "If there are recurrent episodes, the ICD-11 code becomes 6A71"),
        ("300.01", "6B01", "equivalent", "Panic Disorder has direct correspondence"),
        ("300.02", "6B00", "equivalent", "Generalized Anxiety Disorder maps to Generalised anxiety disorder"),
        ("300.23", "6B04", "equivalent", "Social Anxiety Disorder corresponds to Social anxiety disorder"),
        ("309.81", "6B40", "related", "PTSD maps to 6B40, but ICD-11 also has Complex PTSD (6B41) for more severe cases"),
        ("309.81", "6B41", "related", "Complex presentations of PTSD may map to Complex PTSD in ICD-11"),
        ("309.0", "6B43", "equivalent", "Adjustment Disorder has direct correspondence"),
        ("300.3", "6B20", "equivalent", "Obsessive-Compulsive Disorder maps directly"),
        ("314.01", "6A05", "equivalent", "ADHD has direct correspondence, presentation types differ slightly"),
        ("296.41", "6A60", "equivalent", "Bipolar I Disorder corresponds to Bipolar type I disorder"),
        ("296.89", "6A61", "equivalent", "Bipolar II Disorder corresponds to Bipolar type II disorder"),
        ("295.90", "6A20", "equivalent", "Schizophrenia has direct correspondence"),
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO cross_references 
        (dsm5_code, icd11_code, relationship_type, notes)
        VALUES (?, ?, ?, ?)
    """, cross_refs)
    
    conn.commit()
    conn.close()
    print(f"✓ Database populated with {len(dsm5_data)} DSM-5-TR disorders, {len(icd11_data)} ICD-11 disorders, and {len(cross_refs)} cross-references")


if __name__ == "__main__":
    print("Initializing Diagnostic Classification Database...")
    print("=" * 60)
    create_database()
    populate_sample_data()
    print("=" * 60)
    print("✓ Database initialization complete!")
    print(f"Database location: {DATABASE_PATH}")
