import moviepy
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
import random
import math
import time
import numpy as np
from PIL import Image
import cv2
import PIL
import imageio
from skimage.filters import gaussian


from PIL import Image



def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            drr = 0
            if rdn < prob:
                pass
                #output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                pass
                #output[i][j] = image[i][j]
    return output







def clips_old(name, profile, fsm_param):
    if fsm_param == 1:
        clip = VideoFileClip(name+'.mp4')
        clip1 = moviepy.video.fx.all.rotate(clip, random.randint(-10,10))
        clip1.write_videofile(f"{name}_{profile}.mp4")
    elif fsm_param == 2:
        clip = VideoFileClip(name+'.mp4')
        
        clip1 = moviepy.video.fx.all.lum_contrast(clip, lum=random.randint(10,30), contrast=random.randint(10,30), contrast_thr=127)
        clip1.write_videofile(f"{name}_{profile}.mp4")

    elif fsm_param == 3:
        clip = VideoFileClip(name+'.mp4')
        
        clip1 = moviepy.video.fx.all.margin(clip, mar=20, color=(random.randint(10,255), random.randint(10,255), random.randint(10,255)), opacity=1.0)
        clip1.write_videofile(f"{name}_{profile}.mp4")
        



def clips(name, profile, fsm_param = 0):
    defclip = VideoFileClip(name+'.mp4')
    clip = defclip
    rand = [-1,1]
    r_i = random.randint(1,5)
    for i in range(r_i):
        clip1 = moviepy.video.fx.all.margin(clip, mar=3, color=(random.randint(10,255), random.randint(10,255), random.randint(10,255)), opacity=1.0)
        clip = clip1

    clip1 =(clip.fx(vfx.margin , mar=3, color=(random.randint(10,255), random.randint(10,255), random.randint(10,255)), opacity=1.0)
                #.fx(vfx.colorx , (0.9+random.randint(90,110)/100))
                .fx(vfx.lum_contrast , lum=random.randint(75,110)/100, contrast=random.randint(75,110)/100, contrast_thr=127)
                
                )
    
    clip = clip1

    if random.randint(0,1) == 0:
        clip1 = clip.fx(vfx.mirror_x)
        clip = clip1

    clip.write_videofile(f"{name}_{profile}_1.mp4")
    defclip = VideoFileClip(f"{name}_{profile}_1.mp4")
    clip = defclip
    
    clip1 = moviepy.video.fx.all.rotate(clip, (random.randint(1,3)+(random.randint(1,9)/10))*rand[random.randint(0,1)])
    clip = clip1

    #clip1 = moviepy.video.fx.all.margin(clip, mar=3, color=(random.randint(10,255), random.randint(10,255), random.randint(10,255)), opacity=1.0)
    #clip = clip1


    


    ##clip1 = moviepy.video.fx.all.accel_decel(clip, abruptness=math.sqrt(random.randint(1,300)/100), soonness=math.sqrt(random.randint(1,300)/100))
    #clip1 = moviepy.video.fx.all.colorx(clip, 0.7+math.sqrt(random.randint(70,130)/100)/10)

    #clip = clip1

    #clip1 = moviepy.video.fx.all.even_size(clip)

    #clip = clip1
    clip = clip#.set_fps(60)

    noise_strenght = random.randint(15,35)/100

    noise = VideoFileClip('NIWEBM\\noise_web_1_1.webm').set_opacity(noise_strenght).set_duration(clip.duration)
    
    #noise_f = concatenate_videoclips([noise,noise,noise,noise,noise])
    video = CompositeVideoClip([clip,noise])

    video.write_videofile(f"{name}_{profile}.mp4", codec = 'mpeg4')



def clips_res(name, profile, fsm_param = 0):

    time.sleep(20)
    #defclip = VideoFileClip(f"m{fsm_param}_{profile}_1.mp4")
    #defclip.write_videofile(f"m{fsm_param}_{profile}_1.mp4")



def blur(video, param = 2):
    def blurs(image):
        return gaussian(image.astype(float), sigma=random.randint(2,12))


    clip_blured = video.fl_image(blurs)
    return clip_blured
    

def mirror(video, param = 0):
    clip_blured = video.fx(vfx.mirror_x)
    return clip_blured


def contrast(video, param = 0):
    param = int(param)
    clip_contrast = video.fx(vfx.lum_contrast , lum=random.randint(20+param*7,50+param*8)/100, contrast=random.randint(20+param*7,50+param*8)/100, contrast_thr=127)
    return clip_contrast


def margin(video, param = 0):
    clip_margin = video.fx(vfx.margin , mar=3, color=(random.randint(10,255), random.randint(10,255), random.randint(10,255)), opacity=1.0)
    return clip_margin


def rotate(video , param = 0):
    param = int(param)
    rand = [-1,1]
    val = (random.randint(0,param+2)+(random.randint(1,9)/10))*rand[random.randint(0,1)]
    clip = video
    #clip = video.fx(vfx.rotate, val)
    clip_rotate = clip.add_mask().rotate(val)
    return clip_rotate







def parametrick_clip(name, profile, params):
    print(name)
    print(profile)
    print(params)

    name_clip = 'out\\'+f"{name}_{profile}_1.mp4"
    name_final = 'out\\'+f"{name}_{profile}.mp4"


    params = params.split(' ')
    start_clip = VideoFileClip(name+'.mp4')
    clip = start_clip
    #blur
    blur_v = None
    if int(params[3]) == 1:
        print('fffsssssssssssss')
        clip1 = blur(clip, 2)
        clip1.fx(vfx.resize, newsize=1.3)
        #clip.resize(height=1200)
        blur_v = clip1
        #blur_v.write_videofile(f"{name}_{profile}_b.mp4")
    print('fff')



    #margin
    if int(params[1]) !=0:
        r_i = random.randint(1,int(params[1]))
        for i in range(r_i):
            clip1 = margin(clip)
            clip = clip1
    print('fff')

    #contrast
    if int(params[4]) != 0:
        clip1 = contrast(clip, params[4])
    print('fff')

    #mirror
    if int(params[5]) == 1:
        if random.randint(0,1) == 1:
            clip1 = mirror(clip)
            clip = clip1
    elif int(params[5]) == 2:
        clip1 = mirror(clip)
        clip = clip1
    print('fff')
    
    #name_clip = "suka.mp4"

    #start_clip = VideoFileClip(name+'.mp4')
    #clip = start_clip

    

    clip.write_videofile(filename = name_clip, fps = 30, codec = 'mpeg4')
    time.sleep(1)
    restart_clip = VideoFileClip(name_clip)
    clip = restart_clip
    print('fff')

    if int(params[0]) !=0:
        clip1 = rotate(clip, params[0])
        clip = clip1
    print('fff')


    if int(params[2]) != 0:
        params[2] = int(params[2])
        noise_strenght = random.randint(10+params[2],25+params[2]*3)/100

        noise = VideoFileClip('NIWEBM\\noise_web_1_1.webm').set_opacity(noise_strenght).set_duration(clip.duration)
    
        if blur_v != None:
            value = clip.size
            print(value)
            print(value[1])
            clip1 = CompositeVideoClip([blur_v.fx(vfx.resize, height = clip.size[0]*1.2, width = clip.size[1]*1.2), clip.set_position("center"), noise]).set_fps(30)
            clip = clip1
            blur_v = None
        else:
        
            clip1 = CompositeVideoClip([clip,noise])
        clip = clip1

    print('fff')
    print(clip.size)
    if blur_v != None:
        m_blur = blur_v.fx(vfx.resize, height = clip.size[0]*1.2, width = clip.size[1]*1.2)
        m_blur.write_videofile('out\\'+f"blur_{name}_{profile}.mp4", fps = 30, threads=8)
        clip1 = CompositeVideoClip([m_blur, clip.set_position("center")]).fx(vfx.resize, height = clip.size[0]*1.2, width = clip.size[1]*1.2).set_fps(30)
        clip = clip1




    print('111')
    num = random.randint(0,8)
    audio_noise = AudioFileClip(f'FA\\{num}.mp3')
    print('111')
    dur_clip = clip.duration
    dur_audio = audio_noise.duration
    print('111')
    audio1 = audio_noise
    while audio1.duration < dur_clip:
        audio2 = concatenate_audioclips([audio1,audio_noise])
        audio1 = audio2
    print('111')
    audio_noise = audio1.set_duration(dur_clip).volumex(0.3)
    print('111')
    try:
        final_audio = CompositeAudioClip([clip.audio, audio_noise])
    except:
        final_audio = audio_noise
    clip1 = clip.set_audio(final_audio)
    clip = clip1



    #audio_noise
    print('111')
    num = random.randint(0,7)
    audio_noise = AudioFileClip(f'NA\\{num}.mp3')
    print('111')
    dur_clip = clip.duration
    dur_audio = audio_noise.duration
    print('111')
    audio1 = audio_noise
    while audio1.duration < dur_clip:
        audio2 = concatenate_audioclips([audio1,audio_noise])
        audio1 = audio2
    print('111')
    audio_noise = audio1.set_duration(dur_clip).volumex(0.3)
    print('111')

    final_audio = CompositeAudioClip([clip.audio, audio_noise])
    clip1 = clip.set_audio(final_audio)




    #clip1 = CompositeVideoClip([clip,audio_noise])

    clip = clip1

    clip.write_videofile(name_final, fps = 30, threads=8) #, codec = 'mpeg4')





    

if __name__ == '__main__':
    tag = int(input('tag = '))
    
    time.sleep(3)
    a = 0
    if tag == 1:
        for i in range(100):
            print(i)
            #image = Image.open('img_to_noise_2000.png') # Only for grayscale image
            #image = open('img_to_noise_2000.png','r') # Only for grayscale image
            image = cv2.imread('img_to_noise_a1.png',0) # Only for grayscale image
            img = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
            noise_img = sp_noise(img,0.15)
            #noise_img = sp_noise(image,0.2)
            cv2.imwrite(f'NI\\sp_noise_{i+a}.png', noise_img)


        

    elif tag == 2:
        #for i in range(100):
        images = []
        for i in range(600):
            print(i)
            #image = Image.open('img_to_noise_2000.png') # Only for grayscale image
            rand = random.randint(0,99)
            images.append(imageio.imread(f'NI\\sp_noise_{rand}.png'))
    
        i = 1
        print('fff')
        kargs = { 'duration': 1/60 }
        imageio.mimsave(f'NIG\\noise_gif_{i}.gif' , images, 'GIF', **kargs)
        print('fff')
    elif tag == 3:
        i = 1
        clip = VideoFileClip(f'NIG\\noise_gif_{i}.gif').set_fps(60)
        print('fff')
        noise_f = concatenate_videoclips([clip,clip,clip,clip,clip])
        print('fff')

        noise_f.write_videofile(f'NIWEBM\\noise_web_{i}_1.webm')
        
        #clip = VideoFileClip(f'NIWEBM\\noise_web_{i}.webm')
        #clip.write_videofile(f'NIWEBM\\noise_web_{i}.webm')

    elif tag == 4:       
        i = 1
        for i in range(5):
            clips(f'test', f'test_test{i}')


#i=0
#print(i)
#i += 1

