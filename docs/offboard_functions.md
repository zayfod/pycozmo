
Cozmo Off-Board Functions
=========================

Cozmo mobile application resources consist of:
- audio files
- animations
- animation group descriptions
- behaviors
- reaction triggers
- emotions
- activities
- text-to-speech models

Robot firmware images are also distributed as part of the app resources.


Directory structure
-------------------

```
cozmo_resources/
    assets/
        animationGroupMaps/
        animationGroups/
        animations/
        cubeAnimationGroupMaps/
        faceAnimations/
        RewardedActions/
    config/
        engine/
            animations/
            behaviorSystem/
                activities/
                behaviors/
            emotionevents/
            firmware/
            lights/
                backpackLights/
                cubeLights/
    sound/
        English(US)
    tts/
```


Audio files
-----------

### WEM files
### BNK files


Animations
----------

Cozmo "animations" allow animating the following aspects of the robot: 

- body movement
- lift movement
- head movement
- face images
- backpack LED animations
- audio

Cozmo animations are series of keyframes, stored in binary files in [FlatBuffers](https://google.github.io/flatbuffers/)
format. Animation data structures are declared in FlatBuffers format in
`files/cozmo/cozmo_resources/config/cozmo_anim.fbs` . The animation files are available in the following directory of
the Android mobile application:

`files/cozmo/cozmo_resources/assets/animations`

Face images are generated procedurally. They are described by 43 parameters - 5 for the face and 19 for each eye.
The face as a whole can be translated, scaled, and rotated. Each individual eye can be translated, scaled, and rotated.
The 4 corners of each eye can be controlled and each eye has a lower and upper lid.  

The following presentation from Anki provides some background information on Cozmo animations:

[Cozmo: Animation pipeline for a physical robot](https://www.gdcvault.com/play/1024488/Cozmo-Animation-Pipeline-for-a)


Animation groups
----------------

Animation groups are sets of animations with the same purpose.


Behaviors
---------

Behaviors can be thought of as small applications that perform a specific function using the robot client API.


Reactions
---------

Reactions map robot events to behaviors.


Emotions
--------

Emotions are modeled as value functions that change in one of the following ways:
- over time, driven by a decay function
- as a result of reactions
- as a result of behaviors


Activities
----------

Activities are sets of behaviors with a rule how to choose 
