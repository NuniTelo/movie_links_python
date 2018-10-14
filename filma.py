import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify,request,render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/index/<page>')
@cross_origin()
def index(page):
    data_list = []
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
    data = requests.get('http://www.filma24.io/page/' + str(page) , headers = headers) #we make the request first
    soup = BeautifulSoup(data.text, 'html.parser') #now we pass the response to the soup

    #here we filter all the elemenets
    #1.first we save all the names of the movies
    #2.second we save all the links of the movies

    for element in soup.findAll('div', class_ = 'movie-thumb') :
        movie_name = element.find('div', class_='under-thumb').h4.text
        movie_link = element.find('div',class_= 'single-movie').a['href']
        movie_thumbnail =  element.find('div',attrs={'class':'xtt'})
        #append data to list
        # print(movie_thumbnail['style'][21:len(movie_thumbnail['style'])-1])
        if "sez" not in movie_name.lower():
            data_list.append({'name':movie_name,'link':movie_link,'thumbnail':movie_thumbnail['style'][21:len(movie_thumbnail['style'])-1]})

    return jsonify(data_list)

@app.route('/movieInfo',methods = ['GET','POST'])
@cross_origin()
def getMovieLinks():
    link = request.json.get('movieLink')
    print(link)
    list_links_movie = []
    complete_data = []
    data = requests.get(str(link)) #we make the request first
    soup = BeautifulSoup(data.text, 'html.parser') #now we pass the response to the soup
    #now let's pass the data we want
    for el in soup.findAll('a',attrs = {'target' : '_new'}):
        # print(el['href']) # like this we get the link
        list_links_movie.append(el['href'])
        # print(el[''])

    #let us try all this options to see what stream it is
    #that's the link inside the iframe
    video_id_streamango = soup.find('iframe', attrs = {'scrolling' : 'no'})
    print(video_id_streamango['src'])


    #but we may want also the true link of the video
    #a mp4 link so we can play inside out application
    #========================================USE THIS ONLY IF WE NEED MP4 LINK ========================================
    # from selenium import webdriver
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # driver = webdriver.Chrome(executable_path = './chromedriver',chrome_options = options)
    # driver.get(str(video_id_streamango['src']))
    # video_soup = BeautifulSoup(driver.page_source,'html.parser' )
    #
    # div_movie_video_continer = video_soup.find('video', attrs = {'id' : 'mgvideo_html5_api'})
    # print(div_movie_video_continer['src']) #now I have the source
    #========================================USE THIS ONLY IF WE NEED MP4 LINK ========================================


    complete_data.append({'links':list_links_movie, 'iframe': video_id_streamango['src']})


    return jsonify(complete_data)


if __name__ == '__main__':
    app.run()
