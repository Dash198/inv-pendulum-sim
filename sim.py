import gym
import math
import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
x_cart_scale, pendulum_len = 150, 200
cart_width, cart_height = 100, 5
y_cart = height - 100

# Set up the display
scrn = pygame.display.set_mode((width, height))

# Create the CartPole-v1 environment (no need for render_mode)
env = gym.make("CartPole-v1")

# Reset the environment to start
observation, _ = env.reset()

action = env.action_space.sample()

# Game loop
running = True
#taking a random action
action = env.action_space.sample()
integ=0
for _ in range(999):
    scrn.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Take an action (`0` is force to the left, and `1` is force to the right)
    """
    YOUR GOAL IS TO USE REINFORCEMENT LEARNING TO OPTIMISE THE ACTION PICKED
    """

    # Step the environment forward using the selected action
    observation, reward, terminated, truncated, info = env.step(action)
    # observation is [x pos of cart, x vel of cart, pendulum angle (in radians), pendulum angular vel]

    # Unpack observation values
    x_cart = int(observation[0] * x_cart_scale) + width // 2  # Scale and centre the cart
    ang = observation[2]
    ang_vel=observation[3]

    #implementing a pid controller
    integ+=ang
    kp=1
    kd=0.1
    ki=0.001
    u=kp*ang + kd*ang_vel
    if(u>0):
        action=1
    elif(u<0):
        action=0

    # Calculate pendulum position
    x_p = x_cart + pendulum_len * math.sin(ang)
    y_p = y_cart - pendulum_len * math.cos(ang)

    # Draw the pendulum and cart
    pygame.draw.line(scrn, (0, 0, 255), (x_cart, y_cart), (x_p, y_p), 2)
    pygame.draw.circle(scrn, (0, 255, 0), (int(x_p), int(y_p)), 15)
    pygame.draw.rect(scrn, (255, 0, 0), pygame.Rect(x_cart - cart_width // 2, y_cart, cart_width, cart_height))

    # Update the display
    pygame.display.update()

    # Check if the episode is terminated (pole has fallen)
    if terminated:
        print("Pendulum exceeded 12 degrees from the vertical.")  # Considered as fallen over
        observation, _ = env.reset()  # Fix: reset observation correctly

    # Exit the loop if the game is closed
    if not running:
        break

    # Pause for a brief moment (adjustable)
    pygame.time.wait(50)  # in milliseconds

# Close the environment and quit Pygame
env.close()
pygame.quit()
