# PIC 16B Final Project 

## Project Address
The project addresses the growing field of reinforcement learning regarding a self-created video game. I have been interested in reinforcement learning for years because I used to watch YouTube videos about training an agent to play certain games such as Tetris and Snake. I found it fascinating how an algorithm could learn by repeatedly making mistakes to learn and evolve. As a statistics major, I took many courses on supervised learning and even some on unsupervised learning, but nothing in my courses covered reinforcement learning. Since I could not learn about reinforcement learning at UCLA, I took matter into my own hands by taking a Coursera course on it last summer. While I found this course to be informative, I never successfully implemented a reinforcement learning project on my own. Once I found out the layout of this class with a flexible final project, I thought that this would be an excellent opportunity to implement reinforcement learning and learn about it along the way. Since I am familiar with creating 2D platform style video games in Python via PyGame, I figured the optimal way to implement reinforcement learning would be to create my own game and train the agent to complete it. 

## Resources
Due to the inherent nature of reinforcement learning, all the “data” is obtained via present state stimuli. What this means is that at any given state (in the case of a video game this is a frame) important information is passed through a model (usually a neural network) to dictate the agent’s decision. This is all to say, no outside data will be used. However, significant computation power will be used to run the video game and subsequent neural network at each frame. This may cause marginal game lag. 

## Related Work
Since I am created a brand-new video game from scratch, there is no previous work done on exactly my project. However, there is a lot of tangential work that I will be referencing to assist me on my own reinforcement learning project. In particular, there is a project that uses reinforcement learning on the popular game, [Snake](https://www.youtube.com/watch?v=-NJ9frfAWRo)

## Tools and Skills
This project will involve extensive knowledge of 2 Python packages, PyGame for the video game and Tensorflow for deep learning. Since Tensorflow is part of the curriculum for this course, that is where knowledge learned for this course is relevant. Also in a general sense, data wrangling using Pandas and visualization using Seaborn for presentation purposes will be useful. 

## Learning
Since this will be my first-time implementing reinforcement learning from scratch on my own video game, it’s sufficient to say that I will learn a ton about reinforcement learning. I have a grasp on reinforcement learning, but general knowledge and the knowledge it takes to put it into practice are 2 entirely different things. As I come across roadblocks and problems, my knowledge in both reinforcement learning and deep learning will deepen. 

## Group
I am currently working on this individually, but I believe Michael Papagni may join my group eventually. Regardless here is the tentative timeline: 

-	End of Week 7: I have a fully functional 2D platformer with at least 5 levels, but without any reinforcement learning
-	End of Week 8: I have a rough skeleton of classes each in their own python file. There should be 3 1 contains a class for game code, 1 contains a class for deep learning code, and 1 imports both classes to use in sync with each other for reinforcement learning. 
-	End of Week 9: I have a fully functional reinforcement learning algorithm in which the agent is able to complete each level in reasonable time. 
