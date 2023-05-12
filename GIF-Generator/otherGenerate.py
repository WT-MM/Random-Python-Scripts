import cv2
import argparse
import imageio




def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
    
def create_sequential_videos(video_file, num_videos, duration, skipped_frames, video_width, video_height):
    print(f'Creating {num_videos} GIFs from {video_file}...')
    
    # Open the video file
    video = cv2.VideoCapture(video_file, cv2.CAP_FFMPEG)

    # Get the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    video_fps = video.get(cv2.CAP_PROP_FPS)

    # Calculate the number of frames per video
    num_frames_per_video = int(video_fps * duration)

    # Calculate the number of frames between each GIF
    frames_between_gifs = (total_frames - num_frames_per_video * num_videos) // num_videos

    # Loop through each GIF and extract the desired frames
    for i in range(num_videos):
        # Calculate the starting and ending frame indices for this GIF
        start_frame = i * (num_frames_per_video + frames_between_gifs)
        end_frame = start_frame + num_frames_per_video

        # Set the video frame position to the starting frame
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        # Create a list to store the frames for this GIF
        gif_frames = []
        # Loop through the frames and write them to the GIF
        for j in range(0,num_frames_per_video):
            # Read the current frame
            ret, frame = video.read()
            if(j % skipped_frames != 0):
                continue
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = image_resize(frame_rgb, width=video_width)
            #resized = cv2.resize(frame, (video_width, video_height), interpolation = cv2.INTER_AREA)
            gif_frames.append(frame_rgb)
        imageio.mimsave(f'../output/output_{i+1}.gif', gif_frames, duration=duration/len(gif_frames))

    # Release the video and GIF writers
    video.release()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract sequential frames from a video and create multiple GIFs.')
    parser.add_argument('input', type=str, help='path to the input video file')
    parser.add_argument('-n', '--num', type=int, default=8, help='number of output GIFs')
    parser.add_argument('-d', '--duration', type=int, default=5, help='duration of each GIF in seconds')
    parser.add_argument('-s', '--skip', type=int, default=5, help='number of frames to skip during each GIF')
    parser.add_argument('-x', '--width', type=int, default=640, help='width of the output GIFs')
    parser.add_argument('-y', '--height', type=int, default=480, help='height of the output GIFs')
    args = parser.parse_args()

    # Call the function with the provided command line arguments
    create_sequential_videos(args.input, args.num, args.duration, args.skip, args.width, args.height)