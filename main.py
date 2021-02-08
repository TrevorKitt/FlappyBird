import pygame as pg
import sprite_sheet
from settings import *
import os
import random


class Bird(pg.sprite.Sprite):
    def __init__(self, images, app):
        super(Bird, self).__init__()
        self.images = images
        self.app = app
        self.zero()

    def update(self, foreground):
        if self.momentum < 0:
            self.fall_frame_count = 0
            self.frame_counter += 1
            if self.frame_counter == ANIMATION_FRAME_COUNT:
                self.frame_counter = 0
            self.image_index =  int(self.frame_counter / (ANIMATION_FRAME_COUNT / len(self.images)))
            self.image = pg.transform.rotate(self.images[self.image_index], FLIGHT_ROTATION_ANGLE)
        else:
            self.fall_frame_count += 1
            if self.fall_frame_count > 22:
                self.fall_frame_count = 22
            self.image = pg.transform.rotate(self.images[self.image_index], 20 - 5 * self.fall_frame_count)
        self.momentum += BIRD_FALL_SPEED
        if pg.sprite.spritecollide(self, foreground, False):
            self.momentum = 0
            self.app.gameover()
        self.rect = self.rect.move(0,self.momentum)

    def flap(self):
        self.momentum = BIRD_FLAP_MOMENTUM

    def zero(self):
        self.momentum = 0
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.frame_counter = 0
        self.fall_frame_count = 0
        self.rect = pg.Rect((WINDOW_WIDTH - self.images[0].get_width()) / 2, (WINDOW_HEIGHT - self.images[0].get_height()) / 2, BIRD_FULL_SIZE[0], BIRD_FULL_SIZE[1])


class Pipe(pg.sprite.Sprite):
    def __init__(self, image, size, height, id):
        super(Pipe, self).__init__()
        self.image = image
        self.height = height
        self.rect = pg.Rect(WINDOW_WIDTH,height,size[0],size[1])
        self.momentum = FOREGROUND_MOMENTUM
        self.id = id

    def update(self):
        self.rect = self.rect.move(self.momentum, 0)


class Foreground(pg.sprite.Sprite):
    def __init__(self, image, size):
        super(Foreground, self).__init__()
        self.image = image
        self.size = size
        self.position = 0
        self.rect = pg.Rect(self.position, int(3 * WINDOW_HEIGHT/4), self.size[0], self.size[1])

    def update(self):
        self.position += FOREGROUND_MOMENTUM
        if self.position < -WINDOW_WIDTH:
            self.position = 0
        self.rect = pg.Rect(self.position, int(3 * WINDOW_HEIGHT/4), self.size[0], self.size[1])


class OkButton(pg.sprite.Sprite):
    def __init__(self, image, size):
        super(OkButton, self).__init__()
        self.image = image
        self.rect = pg.Rect(250,300, size[0], size[1])


class App:
    def __init__(self):
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()
        self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.size = (self.width, self.height)
        self._display_surf = pg.display.set_mode(self.size)
        self.spriter = sprite_sheet.SpriteSheet(os.path.join("resources", "sprites-edited.png"))
        try:
            with open(os.path.join("resources", "highscore"), 'r') as f:
                self.highscore = int(f.readline())
        except:
            self.highscore = 0
        self.background = pg.Surface(BACKGROUND_SPRITE_SIZE)
        self.background.blit(self.spriter.image_at(pg.Rect(BACKGROUND_SPRITE_LOCATION,BACKGROUND_SPRITE_SIZE)), (0,0))
        self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        foreground = pg.transform.scale(self.spriter.image_at(pg.Rect(FOREGROUND_SPRITE_LOCATION,FOREGROUND_SPRITE_SIZE)), FOREGROUND_FINAL_SIZE)
        doubledForeground = pg.Surface((2* WINDOW_WIDTH, int(WINDOW_HEIGHT/4)))
        doubledForeground.blit(foreground, (0, 0))
        doubledForeground.blit(foreground, (WINDOW_WIDTH, 0))
        self.foreground_group = pg.sprite.Group(Foreground(doubledForeground, (2* WINDOW_WIDTH, int(WINDOW_HEIGHT/4))))

        bird_rects_initial = [pg.Rect(BIRD_SPRITE_LOCATION_1, BIRD_SPRITE_SIZE), pg.Rect(BIRD_SPRITE_LOCATION_2, BIRD_SPRITE_SIZE), pg.Rect(BIRD_SPRITE_LOCATION_3, BIRD_SPRITE_SIZE)]
        bird_images = [pg.transform.scale(image, BIRD_FULL_SIZE) for image in self.spriter.images_at(bird_rects_initial, colorkey=-1)]
        self.bird = Bird(bird_images, self)
        self.bird_group = pg.sprite.Group(self.bird)

        self.pipe_group = pg.sprite.Group()

        self.up_pipe_image = pg.transform.scale(self.spriter.image_at(pg.Rect(83,324,28,160), -1), PIPE_SIZE)
        self.down_pipe_image = pg.transform.scale(self.spriter.image_at(pg.Rect(55,324,28,160), -1), PIPE_SIZE)
        self.score_images = []
        self.score_images.append(pg.transform.scale(self.spriter.image_at(pg.Rect(494,60, NUMBER_SPRITE_WIDTH, NUMBER_SPRITE_HEIGHT), -1), NUMBER_FINAL_SIZE))
        self.score_images.append(pg.transform.scale(self.spriter.image_at(pg.Rect(135,455, 9, 18), -1), (30, 60)))
        self.score_images.append(pg.transform.scale(self.spriter.image_at(pg.Rect(290, 160, NUMBER_SPRITE_WIDTH, NUMBER_SPRITE_HEIGHT), -1), NUMBER_FINAL_SIZE))
        self.score_images.append(pg.transform.scale(self.spriter.image_at(pg.Rect(304, 160, NUMBER_SPRITE_WIDTH, NUMBER_SPRITE_HEIGHT), -1), NUMBER_FINAL_SIZE))
        self.score_images.append(pg.transform.scale(self.spriter.image_at(pg.Rect(318, 160, NUMBER_SPRITE_WIDTH, NUMBER_SPRITE_HEIGHT), -1), NUMBER_FINAL_SIZE))
        self.score_images.append(pg.transform.scale(self.spriter.image_at(pg.Rect(332, 160, NUMBER_SPRITE_WIDTH, NUMBER_SPRITE_HEIGHT), -1), NUMBER_FINAL_SIZE))
        self.score_images.append(pg.transform.scale(self.spriter.image_at(pg.Rect(290, 184, NUMBER_SPRITE_WIDTH, NUMBER_SPRITE_HEIGHT), -1), NUMBER_FINAL_SIZE))
        self.score_images.append(pg.transform.scale(self.spriter.image_at(pg.Rect(304, 184, NUMBER_SPRITE_WIDTH, NUMBER_SPRITE_HEIGHT), -1), NUMBER_FINAL_SIZE))
        self.score_images.append(pg.transform.scale(self.spriter.image_at(pg.Rect(318, 184, NUMBER_SPRITE_WIDTH, NUMBER_SPRITE_HEIGHT), -1), NUMBER_FINAL_SIZE))
        self.score_images.append(pg.transform.scale(self.spriter.image_at(pg.Rect(332, 184, NUMBER_SPRITE_WIDTH, NUMBER_SPRITE_HEIGHT), -1), NUMBER_FINAL_SIZE))

        self.score_images_small = []
        for number in self.score_images:
            self.score_images_small.append(pg.transform.scale(number, NUMBER_FINAL_SIZE_SMALL))

        self.gameover_text = pg.transform.scale(self.spriter.image_at(pg.Rect(395, 58, 96, 30), -1), GAMEOVER_TEXT_SIZE)
        self.final_score_area = pg.transform.chop(pg.transform.scale(self.spriter.image_at(pg.Rect(2, 258, 114, 60), -1), (228, 120)), pg.Rect(24, 0, 138, 0))
        self.new_sprite = pg.transform.scale(self.spriter.image_at(pg.Rect(110, 500, 18, 12), -1), (30, 19))
        self.get_ready = pg.transform.scale(self.spriter.image_at(pg.Rect(292, 58, 96, 30), -1), GAMEOVER_TEXT_SIZE)

        self.restart()

    def add_new_pipes(self):
        if self.most_recent_pipe:
            min_height = max(PIPE_MIN_HEIGHT, self.most_recent_pipe.height + self.distance_from_last_pipe + PIPE_SIZE[1] + PIPE_HEIGHT_OFFSET_CONSTANT)
            max_height = min(PIPE_MAX_HEIGHT, self.most_recent_pipe.height - self.distance_from_last_pipe + PIPE_SIZE[1] - PIPE_HEIGHT_OFFSET_CONSTANT)
        else:
            min_height = PIPE_MIN_HEIGHT
            max_height = PIPE_MAX_HEIGHT
        down_pipe_y = random.randint(min_height, max_height) - PIPE_SIZE[1]
        down_pipe = Pipe(self.down_pipe_image, PIPE_SIZE, down_pipe_y, self.next_pipe_id)
        self.pipe_group.add(down_pipe)
        up_pipe = Pipe(self.up_pipe_image, PIPE_SIZE, down_pipe_y + PIPE_SIZE[1] + PIPE_HEIGHT_GAP, self.next_pipe_id)
        self.pipe_group.add(up_pipe)
        self.most_recent_pipe = down_pipe
        self.distance_from_last_pipe = 0
        self.distance_to_next_pipe = random.randint(MIN_DISTANCE_BETWEEN_PIPES, MAX_DISTANCE_BETWEEN_PIPES)
        self.next_pipe_id += 1

    def remove_old_pipes(self):
        for pipe in self.pipe_group:
            if pipe.rect.bottomright[0] < 0:
                pipe.kill()

    def count_pipes_passed(self):
        for pipe in self.pipe_group:
            if pipe.rect.bottomright[0] < self.bird.rect.bottomleft[0]:
                if self.pipes_passed < pipe.id:
                    self.pipes_passed += 1

    def gameover(self):
        if self.highscore < self.pipes_passed:
            self.highscore = self.pipes_passed
            self.new_highscore = True
        self.is_gameover = True

    def restart(self):
        self.pipe_group.empty()
        self.bird.zero()
        self.pipes_passed = 0
        self.next_pipe_id = 1
        self.distance_from_last_pipe = 0
        self.distance_to_next_pipe = 0
        self.most_recent_pipe = None
        self.is_gameover = False
        self.new_highscore = False
        self.waiting_to_start = True

    def on_event(self, event):
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self._running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if self.waiting_to_start:
                self.waiting_to_start = False
            elif self.is_gameover:
                self.restart()
            else:
                self.bird.flap()

    def on_loop(self):
        self.bird_group.update(self.foreground_group)
        if not self.is_gameover:
            self.foreground_group.update()
            self.pipe_group.update()
            self.distance_from_last_pipe += FOREGROUND_MOMENTUM
            self.distance_to_next_pipe += FOREGROUND_MOMENTUM
            self.remove_old_pipes()
            self.count_pipes_passed()
            if pg.sprite.spritecollideany(self.bird, self.foreground_group):
                self.gameover()
            for pipe in self.pipe_group:
                if pg.sprite.collide_mask(self.bird, pipe):
                    self.gameover()
            if self.distance_to_next_pipe <= 0:
                self.add_new_pipes()

    def display_score(self, score, images, location):
        self._display_surf.blit(images[score % 10], location)
        if score > 9:
            tens = images[int((score % 100)/ 10)]
            self._display_surf.blit(tens, (location[0] - tens.get_width(),location[1]))
            if score > 99:
                hundreds = images[int(score / 100)]
                self._display_surf.blit(hundreds, ((location[0] - tens.get_width()) - hundreds.get_width(),location[1]))

    def on_render(self):
        self._display_surf.blit(self.background, (0, 0))
        self.foreground_group.draw(self._display_surf)
        self.pipe_group.draw(self._display_surf)
        self.bird_group.draw(self._display_surf)
        if self.waiting_to_start:
            self._display_surf.blit(self.get_ready, (80, 200))
        else:
            self.display_score(self.pipes_passed, self.score_images, (200,100))
        if self.is_gameover:
            self._display_surf.blit(self.gameover_text, (80,200))
            self._display_surf.blit(self.final_score_area, (180, 300))
            self.display_score(self.pipes_passed, self.score_images_small, (230, 334))
            self.display_score(self.highscore, self.score_images_small, (230, 376))
            if self.new_highscore:
                self._display_surf.blit(self.new_sprite, (182, 360))
        pg.display.flip()

    def on_cleanup(self):
        try:
            with open(os.path.join("resources", "highscore"), 'w') as f:
                f.write(str(self.highscore))
        except:
            pass
        pg.quit()

    def on_execute(self):
        while self._running:
            for event in pg.event.get():
                self.on_event(event)
            if not self.waiting_to_start:
                self.on_loop()
            self.on_render()
            self.clock.tick(FPS)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
