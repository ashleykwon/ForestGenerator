import networkx as nx
import matplotlib.pyplot as plt
import uvicorn
from fastapi import FastAPI, Request, Response
import json
from pydantic import BaseModel
import torch


app = FastAPI()
publicationDict = torch.load('/Users/ashleykwon/Desktop/Insight Engine Project/publicationDict.json')
collaborationNumDict = torch.load('/Users/ashleykwon/Desktop/Insight Engine Project/collaborationNumDict.json')


class Input(BaseModel):
    author: str

def authorDictionaryGenerator(fileName, authorName):
    '''
    Generates a dictionary whose keys are authors that collaborated with authorName
    and values are their numbers of publications with authorName
    '''
    file = open(fileName, 'r')
    metaData = file.readline()
    authorDict = dict()
    publicationNumsDict = dict()
    while True:
        line = file.readline().strip()
        authorList = line.split(",")
        authorList = [author.strip().replace('\xa0', ' ') for author in authorList]
        if not line:
            break
        if authorName in authorList:
            for author in authorList:
                if author != authorName: #when the author is not the main author the Unity user submitted
                    if author not in authorDict:
                        authorDict[author] = 0
                    authorDict[author] += 1
        for author in authorList:
            if author not in publicationNumsDict:
                publicationNumsDict[author] = 0
            publicationNumsDict[author] += 1
    sortedAuthorList = sorted(authorDict.items(), key = lambda x:x[1], reverse = True)
    authorNames = [x[0] for x in sortedAuthorList]
    authorNames[0] = authorName

    publicationNums = [x[1] for x in sortedAuthorList]
    publicationNums[0] = 0
    publicationNumsPairs = sorted([pair for pair in publicationNumsDict.items() if pair[0] in authorNames], 
                            key = lambda x:x[1], reverse = True)
    totalPublicationNums = [x[1] for x in publicationNumsPairs]
    totalPublicationNums[0] = publicationNumsDict[authorName]
    return [authorNames, publicationNums, totalPublicationNums]



def authorPublicationDictionaryGenerator(fileName):
    file = open(fileName, 'r')
    collaboratedAuthorDict = dict()
    publicationDict = dict()
    collaborationNumDict = dict()
    lineNum = 0
    while lineNum != 24450322:
        line = file.readline().strip()
        lineNum += 1
        if '#*' in line: 
            publication = line.replace('#*','').replace(':','-')
            line = file.readline().strip().replace('#@', '')
            authorList = line.split(",")
            for i in range(len(authorList)):
                author = authorList[i].strip()
                if (author not in collaboratedAuthorDict) and (author not in publicationDict):
                    collaboratedAuthorDict[author] = set()
                    publicationDict[author] = set()
                    collaborationNumDict[author] = dict()
                collaboratedAuthorDict[author].update([auth.strip() for auth in authorList if auth != author])
                publicationDict[author].add(publication)
                for otherAuthor in authorList:
                    otherAuthor = otherAuthor.strip()
                    if otherAuthor != author:
                        if otherAuthor not in collaborationNumDict[author]:
                            collaborationNumDict[author][otherAuthor] = 0
                        collaborationNumDict[author][otherAuthor] += 1
    
    torch.save(collaboratedAuthorDict, '/Users/ashleykwon/Desktop/Insight Engine Project/collaboratedAuthorDict.json')
    torch.save(publicationDict, '/Users/ashleykwon/Desktop/Insight Engine Project/publicationDict.json')
    torch.save(collaborationNumDict, '/Users/ashleykwon/Desktop/Insight Engine Project/collaborationNumDict.json')

    return collaboratedAuthorDict, publicationDict, collaborationNumDict



def makeGraph(sortedAuthorDict, authorName):
    G = nx.DiGraph()
    for author in sortedAuthorDict.keys():
        G.add_edge(author, authorName, weight = sortedAuthorDict[author])
    pos = nx.spring_layout(G, weight='weight')
    nx.draw_networkx(G, pos, with_labels = True)
    edge_labels = dict([((n1, n2), d['weight'])
            for n1, n2, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
            label_pos=0.5, font_size=16, font_weight='bold')
    plt.show()
    return G

def findAuthorRelations(publicationDict, collaborationNumDict, authorName):
    collaborationNumDict = sorted(collaborationNumDict[authorName].items(), key = lambda x:x[1], reverse = True)
    collabNums = [0] + [collab[1] for collab in collaborationNumDict]

    collabAuthors = [collab[0] for collab in collaborationNumDict]

    authorNamePublications = [tuple(publicationDict[authorName])] + [tuple(publicationDict[auth]) for auth in collabAuthors]
    
    collabAuthors = [authorName] + collabAuthors
    totalPublicationNums = [len(elt) for elt in authorNamePublications]

    print(collabAuthors)
    print(collabNums)
    print(authorNamePublications)

    return {'authorNames': collabAuthors, 'collabNums': collabNums, 'totalPublicationTitles': authorNamePublications, 'totalPublicationNums': totalPublicationNums}



@app.put("/generate")
def predict(d:Input):
    author = d.author
    relations = findAuthorRelations(publicationDict, collaborationNumDict, author[:-1])
    print(relations)
    jsonData = json.dumps(relations)
    return jsonData


if __name__ == '__main__':
    uvicorn.run(app, host='10.197.65.79', port=8000)
    # sortedAuthorDict = authorDictionaryGenerator('/Users/ashleykwon/Desktop/Tomasi_Publications.txt', 'C. Tomasi')
    # res = makeGraph(sortedAuthorDict, 'C. Tomasi')
    # print(res)

    # fileName = '/Users/ashleykwon/Desktop/Insight Engine Project/citation-acm-v8.txt'
    # collaboratedAuthorDict, publicationDict, collaborationNumDict = authorPublicationDictionaryGenerator(fileName)
    # collaboratedAuthorDict = torch.load('/Users/ashleykwon/Desktop/Insight Engine Project/collaboratedAuthorDict.json')
    # publicationDict = torch.load('/Users/ashleykwon/Desktop/Insight Engine Project/publicationDict.json')
    # collaborationNumDict = torch.load('/Users/ashleykwon/Desktop/Insight Engine Project/collaborationNumDict.json')
    # findAuthorRelations(publicationDict, collaborationNumDict, 'A. Rubens')
    # print(collaboratedAuthorDict)
    # print(publicationDict)
    # print(collaborationNumDict)
    # authorDictionaryGenerator(fileName, 'S. Gu')