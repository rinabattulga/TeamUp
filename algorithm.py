#algorithm to match students into teams
def algorithm(students, teamSize):
    numStudents = len(students)
    numTeams = int(numStudents / teamSize)
    print(numTeams)
    studentid = []
    
    analyst = []
    a = 0
    leader = []
    l = 0
    diplomat = []
    d = 0
    explorer = []
    e = 0
    
    skill1 = []
    s1 = 0
    skill2 = []
    s2 = 0
    skill3 = []
    s3 = 0
    skill4 = []
    s4 = 0

    for j in range(0, numStudents):
        studentid.append(students[j][0])
        
        #add each student's score in the respective category
        analyst.append([students[j][1], students[j][0]])
        a = a + students[j][1]
        leader.append([students[j][2], students[j][0]])
        l = l + students[j][2]
        diplomat.append([students[j][3], students[j][0]])
        d = d + students[j][3]
        explorer.append([students[j][4], students[j][0]])
        e = e + students[j][4]
        
        skill1.append([students[j][5], students[j][0]])
        s1 = a + students[j][5]
        skill2.append([students[j][6], students[j][0]])
        s2 = l + students[j][6]
        skill3.append([students[j][7], students[j][0]])
        s3 = d + students[j][7]
        skill4.append([students[j][8], students[j][0]])
        s4 = e + students[j][8]
        
    #sort each set from high to low
    analyst.sort(key=lambda x: x[0], reverse=True)
    leader.sort(key=lambda x: x[0], reverse=True)
    diplomat.sort(key=lambda x: x[0], reverse=True)
    explorer.sort(key=lambda x: x[0], reverse=True)
    
    skill1.sort(key=lambda x: x[0], reverse=True)
    skill2.sort(key=lambda x: x[0], reverse=True)
    skill3.sort(key=lambda x: x[0], reverse=True)
    skill4.sort(key=lambda x: x[0], reverse=True)
    
    totalScores = [['a', a], ['l', l], ['d', d], ['e', e]]
    totalSkills = [['s1', s1], ['s2', s2], ['s3', s3], ['s4', s4]]
    totalScores.sort(key=lambda x: x[1])
    totalSkills.sort(key=lambda x: x[1])
    
    #final students by category
    analysts = []
    leaders = []
    diplomats = []
    explorers = []
    
    skills1 = []
    skills2 = []
    skills3 = []
    skills4 = []
    
    #prioritize skillsets with lower total scores
    for k in range(0, 4):
        if totalScores[0][0] == 'a':
            for i in range(0, numTeams):
                analysts.append(analyst[i])
                leader.pop([x[1] for x in leader].index(analyst[i][1]))
                diplomat.pop([x[1] for x in diplomat].index(analyst[i][1]))
                explorer.pop([x[1] for x in explorer].index(analyst[i][1]))
                
        if totalScores[0][0] == 'l':
            for i in range(0, numTeams):
                leaders.append(leader[i])
                analyst.pop([x[1] for x in analyst].index(leader[i][1]))
                diplomat.pop([x[1] for x in diplomat].index(leader[i][1]))
                explorer.pop([x[1] for x in explorer].index(leader[i][1]))
                
        if totalScores[0][0] == 'd':
            for i in range(0, numTeams):
                diplomats.append(diplomat[i])
                leader.pop([x[1] for x in leader].index(diplomat[i][1]))
                analyst.pop([x[1] for x in analyst].index(diplomat[i][1]))
                explorer.pop([x[1] for x in explorer].index(diplomat[i][1]))
                
        if totalScores[0][0] == 'e':
            for i in range(0, numTeams):
                explorers.append(explorer[i])
                leader.pop([x[1] for x in leader].index(explorer[i][1]))
                diplomat.pop([x[1] for x in diplomat].index(explorer[i][1]))
                analyst.pop([x[1] for x in analyst].index(explorer[i][1]))
        
        #Skills prioritization
        if totalSkills[0][0] == 's1':
            for i in range(0, numTeams):
                skills1.append(skill1[i])
                skill2.pop([x[1] for x in skill2].index(skill1[i][1]))
                skill3.pop([x[1] for x in skill3].index(skill1[i][1]))
                skill4.pop([x[1] for x in skill4].index(skill1[i][1]))
                
        if totalSkills[0][0] == 's2':
            for i in range(0, numTeams):
                skills2.append(skill2[i])
                skill1.pop([x[1] for x in skill1].index(skill2[i][1]))
                skill3.pop([x[1] for x in skill3].index(skill2[i][1]))
                skill4.pop([x[1] for x in skill4].index(skill2[i][1]))
        
        if totalSkills[0][0] == 's3':
            for i in range(0, numTeams):
                skills3.append(skill3[i])
                skill1.pop([x[1] for x in skill1].index(skill3[i][1]))
                skill2.pop([x[1] for x in skill2].index(skill3[i][1]))
                skill4.pop([x[1] for x in skill4].index(skill3[i][1]))
                
        if totalSkills[0][0] == 's4':
            for i in range(0, numTeams):
                skills4.append(skill4[i])
                skill1.pop([x[1] for x in skill1].index(skill4[i][1]))
                skill2.pop([x[1] for x in skill2].index(skill4[i][1]))
                skill3.pop([x[1] for x in skill3].index(skill4[i][1]))
                
        totalScores.pop(0)
        totalSkills.pop(0)

    #-----------Creating teams based on the categories-----------
    teams = []
    #reverse order of analysts and diplomats
    analysts.sort(key=lambda x: x[0])
    diplomats.sort(key=lambda x: x[0])
    
    #reverse order of skill2 and skill3
    skills2.sort(key=lambda x: x[0])
    skills3.sort(key=lambda x: x[0])
    
    analystid = [student[1] for student in analysts]
    leaderid = [student[1] for student in leaders]
    diplomatid = [student[1] for student in diplomats]
    explorerid = [student[1] for student in explorers]

    skill1id = [student[1] for student in skills1]
    skill2id = [student[1] for student in skills2]
    skill3id = [student[1] for student in skills3]
    skill4id = [student[1] for student in skills4]
    print(skill1id)
    team = []
    
    #create teams, sort by skill first, then personality trait
    for i in range(1, numTeams + 1):
        team.append(skill1id[0])
        if skill1id[0] in analystid:
            for k in range(0, numTeams):
                if leaderid[k] in skill4id:
                    team.append(leaderid[k])
                    skill4id.pop(skill4id.index(leaderid[k]))
                    break
        elif skill1id[0] in leaderid:
            for k in range(0, numTeams):
                if analystid[k] in skill4id:
                    team.append(analystid[k])
                    skill4id.pop(skill4id.index(analystid[k]))
                    break
        elif skill1id[0] in diplomatid:
            for k in range(0, numTeams):
                if explorerid[k] in skill4id:
                    team.append(explorerid[k])
                    skill4id.pop(skill4id.index(explorerid[k]))
                    break
        else:
            for k in range(0, numTeams):
                if diplomatid[k] in skill4id:
                    team.append(diplomatid[k])
                    skill4id.pop(skill4id.index(diplomatid[k]))
                    break
        skill1id.pop(0)
        if len(team) == 1:
            team.append(skill4id[0])
            skill4id.pop(0)
        team.append(skill2id[0])
        if skill2id[0] in analystid:
            for k in range(0, numTeams):
                if leaderid[k] in skill3id:
                    team.append(leaderid[k])
                    skill3id.pop(skill3id.index(leaderid[k]))
                    break
        elif skill2id[0] in leaderid:
            for k in range(0, numTeams):
                if analystid[k] in skill3id:
                    team.append(analystid[k])
                    skill3id.pop(skill3id.index(analystid[k]))
                    break
        elif skill2id[0] in diplomatid:
            for k in range(0, numTeams):
                if explorerid[k] in skill3id:
                    team.append(explorerid[k])
                    skill3id.pop(skill3id.index(explorerid[k]))
                    break
        else:
            for k in range(0, numTeams):
                if diplomatid[k] in skill3id:
                    team.append(diplomatid[k])
                    skill3id.pop(skill3id.index(diplomatid[k]))
                    break
        skill2id.pop(0)
        if len(team) == 3:
            team.append(skill3id[0])
            skill3id.pop(0)
        teams.append(team)
        team = []
    
    #handle leftover students
    remainder = numStudents - (numTeams * 4)
    if remainder > 0:
        matched = []
        leftover = []
        for team in teams:
            for student in team:
                matched.append(student)
        for student in studentid:
            if student not in matched:
                leftover.append(student)
        while leftover:
            for team in reversed(teams):
                if leftover:
                    team.append(leftover[0])
                    leftover.pop(0)
        
    return teams