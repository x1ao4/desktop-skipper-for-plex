from plexapi.server import PlexServer
import time
import pyautogui

# Set the delay between pyautogui functions
pyautogui.PAUSE = 0.1

# Set the URL and token for the Plex server
PLEX_URL = 'your_plex_server_url'
PLEX_TOKEN = 'your-plex-token'

# Connect to the Plex server
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# Create a set to store sessions that have already been printed
printed_sessions = set()

# Create a dictionary to store marker times
marker_times = {}

# Create a dictionary to store the last check time for each session
last_check_times = {}

# Run the script in an infinite loop
while True:
    # Get the current sessions
    sessions = plex.sessions()

    # Check if there are any sessions
    if sessions:
        # Iterate over all sessions
        for session in sessions:
            # Check if the session has already been printed
            if session.ratingKey not in printed_sessions:
                # Add the session to the set of printed sessions
                printed_sessions.add(session.ratingKey)

                # Get the media being played
                media = session.media[0]

                # Check the media type
                if session.type == 'episode':
                    # Print the TV show title
                    print(f'Now playing: {session.grandparentTitle} - {session.title}')
                elif session.type == 'movie':
                    # Print the movie title
                    print(f'Now playing: {session.title}')
                else:
                    # Unknown media type, do nothing
                    pass

                try:
                    # Get markers based on media type
                    if session.type == 'episode':
                        # Get the episode object
                        episode = plex.fetchItem(session.ratingKey)

                        # Get markers from the episode object
                        markers = episode.markers
                    elif session.type == 'movie':
                        # Get the movie object
                        movie = plex.fetchItem(session.ratingKey)

                        # Get markers from the movie object
                        markers = movie.markers
                    else:
                        markers = []

                    # Get intro and credits markers
                    intro_marker = [marker for marker in markers if marker.type == 'intro']
                    credits_marker = [marker for marker in markers if marker.type == 'credits']

                    # Print marker information
                    if intro_marker:
                        intro_times = []
                        for marker in intro_marker:
                            start_time = marker.start / 1000
                            end_time = marker.end / 1000
                            intro_times.append(f'{time.strftime("%H:%M:%S", time.gmtime(start_time))}-{time.strftime("%H:%M:%S", time.gmtime(end_time))}')
                        print(f'Intro marker: {", ".join(intro_times)}')
                    else:
                        print('Intro marker: None')

                    if credits_marker:
                        credits_times = []
                        for marker in credits_marker:
                            start_time = marker.start / 1000
                            end_time = marker.end / 1000
                            credits_times.append(f'{time.strftime("%H:%M:%S", time.gmtime(start_time))}-{time.strftime("%H:%M:%S", time.gmtime(end_time))}')
                        print(f'Credits marker: {", ".join(credits_times)}')
                    else:
                        print('Credits marker: None')

                    # Store marker times in dictionary
                    marker_times[session.ratingKey] = {
                        'intro': [(marker.start, marker.end) for marker in intro_marker],
                        'credits': [(marker.start, marker.end) for marker in credits_marker]
                    }
                except Exception as e:
                    # An error occurred, print error message
                    print(f'Error: {e}')

                print()
            else:
                # Session has already been printed, check if any markers need to be skipped

                # Get the current play time of the session (in milliseconds)
                current_time = session.viewOffset

                # Check if we have any markers for this session
                if session.ratingKey in marker_times:
                    # Get intro and credits marker times (in milliseconds) for this session 
                    intro_times = marker_times[session.ratingKey]['intro']
                    credits_times = marker_times[session.ratingKey]['credits']

                    # Check if any intro markers need to be skipped 
                    for intro_time in intro_times:
                        if current_time >= intro_time[0] and current_time <= intro_time[1]:
                            # We have reached an intro marker, press enter to skip it

                            pyautogui.press('enter')
                            print('Skipping intro')
                            print()

                            # Remove this intro time from list so we don't skip it again 
                            intro_times.remove(intro_time)

                            break

                    # Check if any credits markers need to be skipped 
                    for credits_time in credits_times:
                        if current_time >= credits_time[0] and current_time <= credits_time[1]:
                            # We have reached a credits marker, press enter to skip it

                            pyautogui.press('enter')
                            print('Skipping credits')
                            print()

                            # Remove this credits time from list so we don't skip it again 
                            credits_times.remove(credits_time)

                            break

            # Update the last check time for the session
            last_check_times[session.ratingKey] = time.time()

    else:
        # No sessions, do nothing
        pass

    # Check if any sessions have stopped playing
    for rating_key, last_check_time in list(last_check_times.items()):
        if time.time() - last_check_time > 5:
            # Session has not been checked for over 5 seconds, assume it has stopped playing
            del last_check_times[rating_key]
            printed_sessions.discard(rating_key)

    # Wait a while before checking again
    time.sleep(0.5)
