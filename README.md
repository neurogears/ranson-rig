# ranson-rig
An interactive visual stimulation rig controllable by OSC using Bonsai and BonVision

## Installation

1. Clone or [download](https://github.com/neurogears/ranson-rig/archive/master.zip) this repository
2. Run the `setup.cmd` script in the `bonsai` folder
3. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and run `uv sync` 
4. Run `Bonsai.exe`

## How to use

1. Open `ranson-rig.bonsai` in the `src/workflows` folder
2. Open `osc-test.py` in the `src/python` folder
3. Start the Bonsai workflow
4. Run the python script to go through a demo sequence of trials

## Protocol

The communication interface between Python/MATLAB and the stimulation rig is built on top of the [OSC](http://opensoundcontrol.org/spec-1_0) real-time protocol over UDP.

A sequence of messages is used to setup the stimuli for each trial, followed by a start message for each trial type. The existing messages and their parameters are detailed below.

### Data Storage

Data storage messages control where logged data is recorded, and specify session and trial identifiers to enable replay of trials in open loop mode.

#### Dataset

This message specifies the root of the dataset, i.e. the volume and file path prefix where all the data will be stored. Replay of trials is only allowed within the same dataset.

* **`/dataset`**
  * **Path** the root path of the dataset where all sessions and trials will be stored

#### Experiment

This message specifies the start of a new session, and provides metadata about animal ID and session start time.

* **`/experiment`**
  * **ExpID** the string containing metadata information about the session, in the following format `yyyy-MM-dd_HH-mm-ss_ID`

### Preloading

Preloading messages control the explicit state of the stimulus cache for heavy stimuli. This allows the experimenter to control when exactly resources are loaded and cleared from memory.

#### Resource

This message declares a new resource in the active set to preload. The resource is not preloaded until the entire set is preloaded.

* **`/resource`**
  * **Path** the path to the resource

#### Preload

Signals that the active resource set should be preloaded into memory.

* **`/preload`** (no arguments)

#### Clear

Signals that all currently preloaded sets should be cleared and unloaded from memory.

* **`/clear`** (no arguments)

### Stimulus Control

Stimulus control includes messages used to setup various stimulus in the passive and go/nogo tasks. They can include both visual and non-visual stimulation, including sine gratings, videos, and later audio and other stimulation types.

#### Replay

This message triggers replay of the specified session and trial number. The dataset is searched for the correct trial, and all metadata used to construct the trial information is used to reconstruct trial conditions. All input data such as wheel movements or licks are replayed following their originally recorded timing.

* **`/replay`**
  * **ExpID** the string used to identify the session metadata, in the following format `yyyy-MM-dd_HH-mm-ss_ID`
  * **Trial** the trial number within the specified session which is to be replayed

#### Gratings

Defines a fully parameterized grating stimulus.

* **`/gratings`**
    * **Placement**
      * **Orientation** the angle of the gratings, in degrees
      * **Diameter** the diameter of the gratings, in degrees of visual field
      * **LocationX** the horizontal position of the gratings, in degrees of visual field
      * **LocationY** the vertical position of the gratings, in degrees of visual field
    * **Parameters**
      * **Contrast** the contrast of the gratings, between zero and one
      * **Opacity** the alpha factor of the gratings, between zero and one
      * **Phase** the starting phase of the gratings, from -180 to 180 degrees
      * **Frequency** the spatial frequency of the gratings, in cycles per degree
      * **Speed** the drifting speed of the gratings, in cycles per second
      * **DutyCycle** the duty cycle for square wave gratings, between zero and one, or NaN for sine gratings
    * **Timing**
      * **Onset** the delay until the gratings appear, in seconds
      * **Duration** the time during which the gratings are visible, in seconds

#### Video

This stimulus type implements visual stimulation with an arbitrary image sequence, loaded from a file or folder with images with the following naming convention frame-***.bmp (or other compatible image format). Multiple videos can play simultaneously and each instance can be parameterized individually with different orientation, position, speed and onset/duration.

* **`/video`**
  * **Placement**
    * **Orientation** the angle of the video quad, in degrees
    * **Width** the extent of the video quad in the horizontal direction, in degrees of visual field
    * **Height** the extent of the video quad in the vertical direction, in degrees of visual field
    * **LocationX** the horizontal position of the gratings, in degrees of visual field
    * **LocationY** the vertical position of the gratings, in degrees of visual field
  * **Parameters**
    * **Loop** one if the video should loop, zero otherwise
    * **PlaybackRate**  the frame rate at which images from the sequence should be played, in Hz
    * **Name** the name of the image sequence to play
  * **Timing**
    * **Onset** the delay until the video appears, in seconds
    * **Duration** the time during which the video is visible, in seconds

#### Pulse Valve

This stimulus type implements a single pulse on the water valve output. Pulse duration must be specified manually in the Behavior board GUI.

* **`/pulseValve`** (no arguments)

#### Start

This message immediately plays the current stimulus set as a passive stimulation trial.

* **`/start`** (no arguments)

#### Success

This message sets the current stimulus set to be played on positive outcomes of operant trials.

* **`/success`** (no arguments)

#### Failure

This message sets the current stimulus set to be played on negative outcomes of operant trials.

* **`/failure`** (no arguments)

### Go/NoGo Task

The Go/NoGo module controls the basic task structure of all Go/NoGo tasks. The general sequence is:

1. Pre-stimulus period
2. Stimulus sequence (t0)
3. Response window (t0 + tResponse)
4. Outcome (Hit, Miss, FalseAlarm, CorrectReject) depending on trial type

#### Go

This message starts a go trial with general control parameters.

* **`/go`**
  * **Suppress Duration** the time, in milliseconds, that  licking activity has to be suppressed before displaying the stimulus
  * **Response Start** start time of the response window, in seconds from start of stimulus presentation
  * **Response Duration** duration of response window for go trials, in seconds
  * **Lick Threshold**: the number of licks required to generate a response. Optionally can be zero for immediate reward delivery

#### NoGo

This message starts a no-go trial with general control parameters.

* **`/nogo`**
  * **Suppress Duration** the time, in milliseconds, that  licking activity has to be suppressed before displaying the stimulus
  * **Response Start** start time of the response window, in seconds from start of stimulus presentation
  * **Response Duration** duration of response window for no-go trials, in seconds
  * **Lick Threshold**: the number of licks required to generate a response. Optionally can be zero for immediate reward delivery

### Maze Control

Maze control includes messages used to specify the positioning of tiles in the VR corridor, and the individual interactions for each tile. Messages should be arranged hierarchically: all interactions for a tile should be declared before the tile declaration; and all the tiles should be declared before the corridor is started. See Python and MATLAB examples for more details.

#### Interaction

The interaction message specifies one interaction which should be active for the next tile.

* **`/interaction`**
  * **Name** the name of the interaction type to activate
  * **Arguments** the variable list of arguments to the interaction

Available interactions and their argument types:
* **`endTrial`**: terminates the current trial when the tile is entered
  * **Delay** the time delay in milliseconds for terminating the trial after entering the tile
* **`endLick`**: terminates the current trial when the tile is activated by licking
  * **Lick Threshold** the number of licks required to activate the tile
  * **Delay** the time delay in milliseconds for terminating the trial after activating the tile
* **`teleportEntry`**: teleports to a specified position in the corridor when the tile is entered
  * **Position** the position, in metric units from the start of the corridor, to which the subject is transported to
  * **Max Activations** the maximum number of times the tile can be activated
* **`teleportLick`**: teleports to a specified position in the corridor when the tile is activated by licking
  * **Position** the position, in metric units from the start of the corridor, to which the subject is transported to
  * **Lick Threshold** the number of licks required to activate the tile
  * **Max Activations** the maximum number of times the tile can be activated
* **`gainEntry`**: change the gain of the rotary encoder when the tile is entered
  * **Gain** the new gain of the rotary encoder
  * **Max Activations** the maximum number of times the tile can be activated
* **`rewardEntry`**: triggers reward delivery when entering the tile
  * **Dwell Time** the time, in milliseconds, that the subject needs to stay on the tile before reward delivery
  * **Max Activations** the maximum number of times the tile can be activated
* **`rewardLick`**: triggers reward delivery when the tile is activated by licking
  * **Lick Threshold** the number of licks required to activate the tile
  * **Max Activations** the maximum number of times the tile can be activated

#### Tile

Specifies the position, extent and appearance of a single portion of the corridor walls. Tiles can be specified in all four walls, or set to face the front of the subject. They can also be made invisible and used for interaction only.

* **`/tile`**
  * **Wall** the type of wall to include (left, right, top, bottom, front)
  * **Position** the position along the visual track where the tile starts, in metric units
  * **Extent** the size of the tile along the visual track, in metric units
  * **Texture** specifies the name of the texture to apply to the tile; if no texture is specified, the tile will be invisible
  
#### Corridor

This message starts a virtual corridor trial but also defines certain general properties of the corridor, such as its length, width and height (wall separation), and the starting location and viewpoint.

* **`/corridor`**
  * **Length** the total length of the corridor, in metric units
  * **Width** the width of the corridor, in metric units
  * **Height** the height of the corridor, in metric units
  * **ViewX** the x-location of the view perspective, in metric units
  * **ViewY** the y-location of the view perspective, in metric units
  * **ViewPosition** the starting position of the view perspective, in metric units
