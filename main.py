import pygame
from config import *
from sprites import *
from videoclassifier import VideoProcessor
import sys
import sys
from datetime import datetime

class ExerciseDisplay:
    def __init__(self,classifier):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Exercise Display')
        self.running = True
        self.exercises = self.get_exercises()
        self.font = pygame.font.Font(None, 36)
        self.exercise_surface = pygame.Surface((200,200))
        self.exercise_rect = self.exercise_surface.get_rect(center=(320, 240))
        self.current_exercise = None
        self.classifier = classifier
        

    def get_exercises(self):
        exercises = [
            "Jumping Jacks",
            "Push Ups",
            "Squats",
            "Lunges",
            "Plank",
            "Bicycle Crunches",
            "Deadlift",
            "Leg Press",
            "Shoulder Press",
            "Leg Curl"
        ]
        return exercises

    def display_exercise(self):
        if self.current_exercise is None:
            self.current_exercise = self.classifier.process_video()
        text = self.font.render(self.current_exercise, True, (255, 255, 255))
        text_rect = text.get_rect(center=(320,240))
        self.exercise_surface.blit(text, text_rect)
        self.screen.blit(self.exercise_surface, self.exercise_rect)
        pygame.display.flip()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet('./img/character.png')
        self.terrain_spritesheet = Spritesheet('./img/terrain.png')
        #self.classifier = Classifier("./HAR/resnet-34_kinetics.onnx")
        self.classifier = VideoProcessor()
        self.exercise_display = ExerciseDisplay(self.classifier)

    def new(self):
        # a New Game
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemy_sprites = pygame.sprite.LayeredUpdates()
        self.attack = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j,column in enumerate(row):
                Ground(self,j,i)
                if column == "B":
                    Block(self,j,i)
                if column == "P":
                    Player(self,j,i)

    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        #game loop update
        self.all_sprites.update()


    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.exercise_display.display_exercise()
        self.classifier.release()
        self.running = False

    def game_over(self):
        return

    def intro_screen(self):
        pass

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()