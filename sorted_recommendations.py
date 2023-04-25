import requests_with_caching
import json

#Gets a shorted list of movie recommendations based on an input list of movies
def get_sorted_recommendations (movie_titles_list):
    
    related_movie_list=get_related_titles(movie_titles_list)
    ratings_list=[]
    for movie in related_movie_list:
        ratings_list.append(get_movie_rating(get_movie_data(movie)))
    unsorted_related_movies_list=list(zip(ratings_list,related_movie_list))
    sorted_related_movies_list=sorted(unsorted_related_movies_list, reverse=True)
    sorted_movies=[item[1] for item in sorted_related_movies_list]
    return list(sorted_movies)

#Uses the OMBD API to retrieve movie ratings
def get_movie_data(movie_title):
    baseurl="http://www.omdbapi.com/"
    params={}
    params["t"]=movie_title
    params["r"]="json"
    response=requests_with_caching.get(baseurl, params)
    
    return response.json()

#Extracts the Rotten Tomatoes Rating from the OMDB dictionary
def get_movie_rating(omdb_dict):
    #print(omdb_dict["Ratings"])
    ratings=omdb_dict["Ratings"]
    Rotten_Tomatoes_Ratings=[rt_rating['Value'] for rt_rating in ratings if rt_rating["Source"]=="Rotten Tomatoes"]
    if Rotten_Tomatoes_Ratings==[]:
        rating= 0
    else:
        
        rating = int(Rotten_Tomatoes_Ratings[0].strip('%'))
    return rating

# Uses the TasteDive API to find a list of recommendations 
def get_movies_from_tastedive(name):
    baseurl="https://tastedive.com/api/similar"
    params={}
    params["q"]=name
    params["type"]="movies"
    params["limit"]=5
    response=requests_with_caching.get(baseurl, params)
   
    return response.json()

# Extracts movie titles from TasteDive dictionary
def extract_movie_titles(response):
    results=response['Similar']['Results']
    movie_list=[movie_result['Name'] for movie_result in results ]    
    return movie_list

# Gets a list of unique movie titles related to the input list
def get_related_titles(movie_titles):
    related_titles=[]
    for title in movie_titles:
        tastedive_response=get_movies_from_tastedive(title)
        movie_list=extract_movie_titles(tastedive_response)
        related_titles=related_titles+movie_list
        
    return list(set(related_titles))
