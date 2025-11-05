import argparse,os
import numpy as np
# import matplotlib.pyplot as plt
import gymnasium as gym
import cma



class Policy:
    # Simple one-hidden-layer MLP whose parameters live in a flat vector.
    def __init__(self, obs_size, act_size, hidden=32):
        self.obs, self.act, self.hid = obs_size, act_size, hidden
        self.n_params = hidden * obs_size + hidden + act_size * hidden + act_size  # W1, b1, W2, b2

    def decode(self, w):
        o, h, a = self.obs, self.hid, self.act
        i = 0
        W1 = w[i:i + h * o].reshape(h, o); i += h * o
        b1 = w[i:i + h];                  i += h
        W2 = w[i:i + a * h].reshape(a, h); i += a * h
        b2 = w[i:i + a]

        def π(obs):
            x = np.tanh(W1 @ obs + b1)
            logits = W2 @ x + b2

            if a > 1:
                # Discrete action, return an int
                return int(np.argmax(logits))
            else:
                # Continuous action, return a 1‐element array
                val = float(np.clip(logits, -1, 1))
                return np.array([val])
        return π



def episode_return(env_id, weights, episodes=1, seed=None):
    env = gym.make(env_id)
    if seed is not None:
        env.reset(seed=seed)
    obs_size = env.observation_space.shape[0]
    act_size = env.action_space.n if hasattr(env.action_space, "n") else 1
    policy = Policy(obs_size, act_size).decode(weights)

    total = 0.0
    for _ in range(episodes):
        obs, _ = env.reset()
        done, truncated = False, False
        while not (done or truncated):
            obs, r, done, truncated, _ = env.step(policy(obs))
            total += r
    env.close()
    return total / episodes


def evolutionary_run(env_id, generations=100, pop=64, sigma=0.5, seed=0):
    env = gym.make(env_id)
    obs, act = env.observation_space.shape[0], (env.action_space.n if hasattr(env.action_space, "n") else 1)
    env.close()
    policy = Policy(obs, act)
    es = cma.CMAEvolutionStrategy(policy.n_params * [0.0], sigma,
                                  {"popsize": pop, "seed": seed})
    best_curve = []
    for g in range(generations):
        solutions = es.ask()
        fitness = [-episode_return(env_id, w, seed=seed + g) for w in solutions]  # minimizes
        es.tell(solutions, fitness)
        best_curve.append(-min(fitness))
        print(f"[{env_id}] Gen {g:3d}  best R = {best_curve[-1]:.1f}")
    return best_curve


def multi_seed(env_id, seeds, generations, pop):
    curves = [evolutionary_run(env_id, generations, pop, seed=s) for s in seeds]
    # pad shorter runs if any
    G = max(len(c) for c in curves)
    averaged = [np.mean([c[g] if g < len(c) else c[-1] for c in curves]) for g in range(G)]
    return curves, averaged


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--env", default="CartPole-v1")
    p.add_argument("--generations", type=int, default=100)
    p.add_argument("--pop", type=int, default=64)
    p.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    p.add_argument("--out", default="results")
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    curves, avg = multi_seed(args.env, args.seeds, args.generations, args.pop)

    # # plot
    # plt.figure()
    # for c in curves:
    #     plt.plot(c, alpha=0.3)
    # plt.plot(avg, linewidth=2, label="average")
    # plt.xlabel("generation"); plt.ylabel("episode return"); plt.title(args.env)
    # plt.legend(); plt.tight_layout()
    # plt.savefig(os.path.join(args.out, f"{args.env}_curve.png"))

if __name__ == "__main__":
    main()
    #print(Script started)

