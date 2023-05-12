import cv2
import argparse


def create_sequential_gifs(video_file, num_gifs, num_frames_per_gif, gif_width, gif_height):
    # Open the video file
    video = cv2.VideoCapture(video_file)

    # Get the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the number of frames between each GIF
    frames_between_gifs = (total_frames - num_frames_per_gif * num_gifs) // num_gifs

    # Create a GIF writer for each output file
    gif_writers = []
    for i in range(num_gifs):
        gif_writer = cv2.VideoWriter(f'../output/output_{i+1}.gif', cv2.VideoWriter_fourcc(*'GIF'), 10, (gif_width, gif_height))
        gif_writers.append(gif_writer)

    # Loop through each GIF and extract the desired frames
    for i in range(num_gifs):
        # Calculate the starting and ending frame indices for this GIF
        start_frame = i * (num_frames_per_gif + frames_between_gifs)
        end_frame = start_frame + num_frames_per_gif

        # Set the video frame position to the starting frame
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        # Loop through the frames and write them to the GIF
        for j in range(num_frames_per_gif):
            # Read the current frame
            ret, frame = video.read()

            # Resize the frame to the desired GIF size
            frame = cv2.resize(frame, (gif_width, gif_height))

            # Write the frame to the current GIF
            gif_writers[i].write(frame)

    # Release the video and GIF writers
    video.release()
    for gif_writer in gif_writers:
        gif_writer.release()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract sequential frames from a video and create multiple GIFs.')
    parser.add_argument('input', type=str, help='path to the input video file')
    parser.add_argument('-n', '--num', type=int, default=8, help='number of output GIFs')
    parser.add_argument('-f', '--frames', type=int, default=120, help='number of frames to extract for each GIF')
    parser.add_argument('w', '--width', type=int, default=640, help='width of the output GIFs')
    parser.add_argument('h', '--height', type=int, default=480, help='height of the output GIFs')
    args = parser.parse_args()

    # Call the function with the provided command line arguments
    create_sequential_gifs(args.input, args.num, args.frames, args.width, args.height)