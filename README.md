# PIC 16B Final Project EDITED

## Project Address
Our project addresses the growing field of reinforcement learning regarding a self-created video game. Stephen has been interested in reinforcement learning for years because he used to watch YouTube videos about training an agent to play certain games such as Tetris and Snake. Stephen found it fascinating how an algorithm could learn by repeatedly making mistakes to learn and evolve. As a statistics major, he took courses that involved supervised learning and unsupervised learning, but nothing in his courses covered reinforcement learning. He took matter into his own hands by taking a Coursera course on it last summer, but never successfully implemented a reinforcement learning project on his own. Since this class has a flexible final project, Stephen thought this would be an excellent opportunity to implement reinforcement learning and learn about it along the way. Since he is familiar with creating 2D platform style video games in Python via PyGame, he figured the optimal way to implement reinforcement learning would be to create his own game and train the agent to complete it. Additionally, Michael and Arianna joined the project around Week 7, and together we pursued the shared goal of creating a video game and a reinforcement learning model.

## Resources
Due to the inherent nature of reinforcement learning, all the “data” is obtained via present state stimuli. What this means is that at any given state (in the case of a video game this is a frame) important information is passed through a model (usually a neural network) to dictate the agent’s decision. This is all to say, no outside data will be used. However, significant computation power will be used to run the video game and subsequent neural network at each frame. This may cause marginal game lag. 

## Related Work
Since we are creating a brand-new video game from scratch, there is no previous work done on our project. However, there is a lot of tangential work that we will be referencing to assist us. There is a project that uses reinforcement learning on the popular game, [Snake](https://www.youtube.com/watch?v=-NJ9frfAWRo). 

## Tools and Skills
This project will involve extensive knowledge of PyGame for the video game and TensorFlow for deep learning. Our knowledge for TensorFlow and PyGame will be from this course, with Stephen having previous experience with PyGame from a previous project. Also in a general sense, data wrangling using Pandas and visualization using Seaborn will be useful. While there is no data in a traditional sense, stimuli will need to be processed in a manner feedable to a model. Seaborn will also created informative visualizations comparing model performance on each level. 

## Learning
Since this was our first time implementing reinforcement learning from scratch on our own video game, we learned a lot about reinforcement learning through trial and error. As we came across roadblocks and problems, our knowledge in both reinforcement learning and deep learning in general deepened. 

## Group Contributions Statement
Our group consists of Michael Papagni, Stephen Yu, and Arianna Zhou. Here is a split of group member contributions: 

**Michael Papagni:**
- Implemented the graphics and controls of the video game using PyGame (Weeks 7-8)
- Made and experimented with models and mutation/propogation functions; implemented sight rays (Week 9)
- Ran and compared results of models; contributed to presentation (Week 10)

**Stephen Yu:**
- Completed 5 initial game levels (Week 8)
- Made a second model; adapted the mutation and propogation functions (Week 9)

**Arianna Zhou:**
- Contributed with propogation/model selection functions (Week 8)
- Made a third model (Week 9)
- Made the presentation (Week 10)

*Initial Plan*
-	End of Week 7: We have a fully functional 2D platformer with at least 5 levels, but without any reinforcement learning
-	End of Week 8: We have a rough skeleton of classes, each in their own python file. There should be 1 that contains a class for game code, 1 that contains a class for deep learning code, and 1 that imports both classes to use in sync with each other for implementation. 
-	End of Week 9: We have a fully functional reinforcement learning algorithm in which the agent can complete each level in reasonable time.

## [GitHub Link](https://github.com/stephenyu2/pic16b-final-project) 
