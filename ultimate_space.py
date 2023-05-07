#Script to put spaces in the right places
pipeline_stages = input("Pipeline Stages: ")
pipeline_stages = "F-D-E1-E2-E3-M1-M2-M3-M4-W" if pipeline_stages == "" else pipeline_stages

pipeline_stages = pipeline_stages.split("-")
for i in range(len(pipeline_stages)):
    c = pipeline_stages[i]
    if len(c) == 1:
        pipeline_stages[i] = c + " "
        
print(", ".join(pipeline_stages))