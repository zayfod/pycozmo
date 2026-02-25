import pycozmo

if __name__ == "__main__":
    robot = pycozmo.Client()
    robot.start()
    robot.connect()
    robot.wait_for_robot()
    robot.set_volume(50000)
    # Use espeakng
    robot.say_text(txt="Hello World, My name is Cozmo!")
    robot.wait_for(pycozmo.event.EvtAudioCompleted)
    # Use chatterbox AI model to replicate cozmos voice. !!Uses HIGH RAM and CPU ussage!! -> Make sure you have ran pycozmo_load_voice_model.py while in venv atleast once to download model.
    robot.say_text(txt="Hello World, My name is Cozmo!", cozmo_voice=True)
    robot.wait_for(pycozmo.event.EvtAudioCompleted)