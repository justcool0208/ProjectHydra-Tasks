# Task 3-A: Introduction to Reinforcement Learning Fundamentals

## Objective
This task introduces you to the core concepts of Reinforcement Learning (RL) that form the foundation for building self-healing systems. You will learn about agents, environments, rewards, and policies through hands-on coding exercises using simple, beginner-friendly environments.

## What You'll Build
- A simple grid world environment from scratch
- A random agent baseline
- Q-Learning algorithm implementation
- Understanding of how RL agents learn through trial and error

**This is a learning task** - you're building foundational RL knowledge that will be used in later tasks to create the self-healing system.

---

## What You Need to Learn

### 1. Core RL Concepts
Understand the fundamental building blocks:
- **Agent**: The learner/decision maker
- **Environment**: The world the agent interacts with
- **State**: Current situation/observation
- **Action**: What the agent can do
- **Reward**: Feedback signal (positive/negative)
- **Policy**: Strategy for selecting actions
- **Episode**: One complete interaction sequence

### 2. RL vs Other ML Paradigms
- Compare RL with supervised and unsupervised learning
- Understand why RL is suitable for sequential decision-making problems
- Learn about the exploration vs exploitation trade-off

---

## Hands-On Exercises

### Exercise 1: Simple Grid World Environment
Create a simple 2D grid world where:
- Agent starts at position (0, 0)
- Goal is at position (4, 4)
- Agent can move: UP, DOWN, LEFT, RIGHT
- Reward: +10 for reaching goal, -1 for each step
- Episode ends when goal is reached or after 50 steps

**Deliverable:**
- Python script implementing the grid world environment
- Manual policy demonstration (hardcoded path to goal)
- Visualization showing agent's path

**Tools to use:**
- NumPy for grid representation
- Matplotlib for visualization

---

### Exercise 2: Random Agent Baseline
Implement a random agent that:
- Takes random actions in the grid world
- Tracks total rewards per episode
- Runs for 100 episodes and reports average reward

**Deliverable:**
- Code for random agent
- Statistics: average reward, average episode length, success rate

---

### Exercise 3: Introduction to Gymnasium (OpenAI Gym)
- Install `gymnasium` (formerly OpenAI Gym)
- Run the **CartPole** environment:
  - Understand state space (4 values: position, velocity, angle, angular velocity)
  - Understand action space (2 actions: left/right)
  - Run a random agent for 10 episodes
  - Observe and log rewards

**Deliverable:**
- Code using gymnasium
- Screenshots/videos of agent behavior
- Summary of observations (state ranges, reward structure)

---

### Exercise 4: Simple Q-Learning (Tabular)
Implement a basic Q-Learning algorithm for a small environment:
- Use a **FrozenLake** environment from gymnasium (4x4 grid)
- Implement Q-table (state-action value table)
- Update rule: Q(s,a) = Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
- Use ε-greedy exploration (start with ε=1.0, decay to 0.01)

**Important parameters:**
- Learning rate (α): Start with 0.1
- Discount factor (γ): Use 0.99
- Epsilon decay: Linearly decay from 1.0 to 0.01 over episodes

**Success rate definition**: Percentage of episodes where the agent reaches the goal (not falling into holes)

**Deliverable:**
- Q-Learning implementation from scratch (using NumPy, no RL libraries)
- Training loop that runs for 1000 episodes
- Plot showing:
  - Average reward per episode (moving average over last 50 episodes)
  - Success rate over time (percentage of successful episodes in each window)
  - Final Q-table visualization (heatmap or table showing Q-values)
- Test the trained agent for 10 episodes (with ε=0, no exploration) and report success rate

---

## Resources

1. **RL Introduction Videos:**
   - [Reinforcement Learning: Crash Course AI #9](https://www.youtube.com/watch?v=JgvyzIkgxF0)
   - [An Introduction to Reinforcement Learning](https://www.youtube.com/watch?v=JgvyzIkgxF0)

2. **Q-Learning Tutorial:**
   - [Q-Learning Explained](https://www.youtube.com/watch?v=qhRNvCVVJaA)
   - [Q-Learning Algorithm](https://www.geeksforgeeks.org/q-learning-in-python/)

3. **Gymnasium Documentation:**
   - [Gymnasium Documentation](https://gymnasium.farama.org/)
   - [Gymnasium Environments](https://gymnasium.farama.org/environments/classic_control/)

---

## Deliverables

1. **Grid World Implementation** (Exercise 1)
   - Code file: `grid_world.py`
   - Visualization output

2. **Random Agent Baseline** (Exercise 2)
   - Code file: `random_agent.py`
   - Performance statistics

3. **Gymnasium Introduction** (Exercise 3)
   - Code file: `gymnasium_intro.py`
   - Observations and screenshots

4. **Q-Learning Implementation** (Exercise 4)
   - Code file: `q_learning.py`
   - Training plots
   - Final Q-table
   - Test results

5. **README.md** explaining:
   - What you learned about RL concepts
   - How Q-Learning works
   - Observations from each exercise
   - Challenges faced and solutions

---

## Success Criteria

- [ ] Grid world environment implemented and visualized
- [ ] Random agent baseline established
- [ ] Successfully ran CartPole and FrozenLake environments
- [ ] Q-Learning algorithm implemented from scratch
- [ ] Trained agent achieves >70% success rate on FrozenLake
- [ ] All code is well-documented and organized

---


