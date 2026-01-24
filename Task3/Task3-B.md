# Task 3-B: Deep Reinforcement Learning with Stable Baselines3

## Objective
Move beyond tabular methods to Deep Reinforcement Learning (DRL). You will learn to use **Stable Baselines3**, a popular RL library, to train agents on more complex environments. This task focuses on understanding DQN (Deep Q-Network) and PPO (Proximal Policy Optimization) algorithms, which are essential for the chaos engineering application.

## What You'll Build
- DQN and PPO agents trained on standard environments (CartPole)
- A custom resource management environment
- Comparison of different RL algorithms
- Understanding of how to use RL libraries for real applications

**This builds on Task 3-A** - you'll use the concepts learned there, but now with neural networks and production-ready libraries.

---

## Prerequisites
- Completion of Task 3-A (understanding of basic RL concepts, Q-Learning)
- Familiarity with neural networks (from Task 1-A or Task 2)
- Basic understanding of PyTorch or TensorFlow (Stable Baselines3 uses PyTorch)

---

## What You Need to Learn

### 1. Deep Q-Network (DQN)
- Why we need function approximation (vs tabular Q-learning)
- Experience replay buffer
- Target network for stable training
- Loss function: Mean Squared Error between Q-values

### 2. Policy Gradient Methods
- Policy-based vs value-based methods
- Introduction to PPO (Proximal Policy Optimization)
- Advantages of PPO for continuous and discrete action spaces

### 3. Stable Baselines3
- Installation and basic usage
- Training and evaluation workflows
- Hyperparameter tuning
- Model saving and loading

---

## Hands-On Exercises

### Exercise 1: DQN on CartPole
Train a DQN agent on the CartPole environment:
- Use `stable_baselines3.DQN`
- Train for 10,000 timesteps
- Evaluate the trained agent for 10 episodes
- Compare with random agent performance

**Deliverable:**
- Training code using Stable Baselines3
- Training curves (reward over time)
- Evaluation results (average reward, success rate)
- Video/gif of trained agent in action

---

### Exercise 2: PPO on CartPole
Train a PPO agent on the same CartPole environment:
- Use `stable_baselines3.PPO`
- Train for 10,000 timesteps
- Compare training stability and sample efficiency with DQN

**What to compare:**
- **Training stability**: Does reward increase smoothly or fluctuate?
- **Sample efficiency**: How quickly does each algorithm reach good performance?
- **Final performance**: Which achieves higher average reward?

**Deliverable:**
- Training code for PPO
- Comparison plots: DQN vs PPO (reward curves on same graph)
- Analysis of differences in training behavior (which trains faster, which is more stable)

---

### Exercise 3: Custom Environment - Simple Resource Manager
Create a custom gymnasium environment that simulates a simple resource management scenario:
- **State**: Current CPU usage (0-100%), Memory usage (0-100%), Request rate
- **Actions**: 
  - Scale up (add 1 instance)
  - Scale down (remove 1 instance)
  - Do nothing
- **Reward**: 
  - +10 if CPU/Memory in optimal range (30-70%)
  - -5 if over-utilized (>90%) or under-utilized (<10%)
  - -1 for each action (to encourage efficiency)
- **Episode**: Runs for 100 steps, simulates random workload fluctuations

**Implementation details:**
- Start with 2 instances (replicas)
- Minimum 1 instance, maximum 5 instances
- Each step: workload changes randomly (±20% of current request rate)
- CPU/Memory usage calculated based on: `usage = request_rate / num_instances * base_factor`
- Use `gymnasium.spaces.Box` for state space (3 continuous values)
- Use `gymnasium.spaces.Discrete` for action space (3 actions)

**Deliverable:**
- Custom environment class inheriting from `gymnasium.Env`
- Implement `reset()`, `step(action)`, `render()` methods
- Environment registration and testing (verify it works with random agent)
- Visualization of state transitions (plot CPU/memory over time)
- Documentation of state/action/reward spaces (dimensions, ranges, meanings)

---

### Exercise 4: Train RL Agent on Custom Environment
Train both DQN and PPO on your custom resource manager environment:
- Train each algorithm for 20,000 timesteps
- Tune hyperparameters (learning rate, batch size)
- Compare which algorithm performs better

**Policy behavior analysis**: After training, run the agent for 10 episodes and observe:
- What actions does it take in different states?
- Does it learn to maintain optimal resource usage?
- Does it avoid unnecessary scaling actions?
- Create a plot showing: state (CPU/Memory) → action taken

**Deliverable:**
- Training code for both algorithms
- Training curves (reward over time for both)
- Evaluation: average reward over 10 test episodes
- Policy behavior analysis (action distribution, state-action mapping)
- Discussion of which algorithm works better and why (consider: training speed, final performance, stability)

---

### Exercise 5: Hyperparameter Tuning
Experiment with hyperparameters for PPO:
- Learning rate: [1e-4, 3e-4, 1e-3]
- Batch size: [32, 64, 128]
- Network architecture: [64, 128] vs [128, 256] hidden units

**Deliverable:**
- Hyperparameter sweep results
- Best configuration identified
- Analysis of how hyperparameters affect training

---

## Resources

1. **DQN Paper:**
   - [Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236)

2. **PPO Paper:**
   - [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)

3. **Stable Baselines3:**
   - [Stable Baselines3 Documentation](https://stable-baselines3.readthedocs.io/)
   - [Stable Baselines3 GitHub](https://github.com/DLR-RM/stable-baselines3)
   - [RL Baselines3 Zoo](https://github.com/DLR-RM/rl-baselines3-zoo)

4. **Custom Environments:**
   - [Creating Custom Gymnasium Environments](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/)

---

## Deliverables

1. **DQN Implementation** (Exercise 1)
   - Code: `dqn_cartpole.py`
   - Training curves and evaluation results

2. **PPO Implementation** (Exercise 2)
   - Code: `ppo_cartpole.py`
   - Comparison with DQN

3. **Custom Environment** (Exercise 3)
   - Code: `resource_manager_env.py`
   - Environment testing and visualization

4. **RL Training on Custom Environment** (Exercise 4)
   - Code: `train_resource_manager.py`
   - Training results and analysis

5. **Hyperparameter Tuning** (Exercise 5)
   - Code: `hyperparameter_tuning.py`
   - Results and best configuration

6. **README.md** explaining:
   - Differences between DQN and PPO
   - How to create custom environments
   - Observations from training
   - Best practices for RL training

---

## Success Criteria

- [ ] Successfully trained DQN on CartPole
- [ ] Successfully trained PPO on CartPole
- [ ] Created custom resource manager environment
- [ ] Trained RL agent on custom environment
- [ ] Performed hyperparameter tuning
- [ ] All code is well-documented
- [ ] Can explain differences between DQN and PPO

---


