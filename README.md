# FCP - Simulating COVID-19

## Authors 
Abbie Backers, Adam Morris, Josh Smith, Ollie Hooper

## Installation

*Note: You will need python 3.8 or later to be able to run this program*	

Clone repo from git hub on your local git bash terminal: https://github.com/Ollie-Hooper/COVIDSimulator

Use the following pip commands to install the packages and libaries required to run the file: 

```bash
pip install -r requirements.txt
```

## Usage

Run the following command in your git bash terminal to activate the web-app:

```bash
python main.py
```

Once the web-app has appeared in your browser, enter the desired values into the input boxes.

To run the animation, click the run/save animation button.

To view the plot change over time as a series of images, click the plot button.

To save either of these, enter a name into the appropriate text box, followed by the buttons.

To check that the app is generating these animations/plots you can check that the tab name is showing "Updating...".

## Quick Example

Opening the web-app for the first time you will see the following:

![Quick Example -  Default Parameters](https://github.com/Ollie-Hooper/COVIDSimulator/blob/master/web_app/assets/parameters.png?raw=true)

Clicking the Run/Save animation and the plot button, with the given default parameters, we produce the following output:

![Quick Example - Outputs](https://github.com/Ollie-Hooper/COVIDSimulator/blob/master/web_app/assets/results.png?raw=true)

These outputs are displayed clearly below the inputs section of the web-app. The animation will keep repeating until the parameters are changed and the animation re-loaded, or the web-app is closed.

## Features
The project contains a few different features available to the user, these include: 

 - A huge range of inputs that the user can alter to produce different results
 - Optional counter-epidemic measures based on real-life government procedures
 - The ability to locally save plots 
 
## Contribution
This project is an example of how simulations can be used to try to predict the behaviour of different viruses.

Although this model is fairly simple, the implementation of additional features and parameters to create a more realistic model would be possible. 

Therefore, if you would like to contribute towards this project, or use it in some way to create further models, feel free to use the contact details below to let us know.  

## Contact

 - Adam Morris - ks20447@bristol.ac.uk
 - Ollie Hooper - ollie.hooper.2020@bristol.ac.uk
 - Abbie Backers - ms19248@bristol.ac.uk
 - Josh Smith - de20812@bristol.ac.uk

## Credit
This project was built upon a COVID simulator created by Oscar Benjamin.
