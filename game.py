# game.py
import random
import pygame

MAX_ENERGY = 5

SKILL_EVENTS = [
    {
        "id": "library_group",
        "text": "You run into a study group at the HFU library.",
        "requirements": {"social": 3, "energy": 1},
        "on_success": {
            "knowledge": 2,
            "social": 1,
            "energy": -1,
            "message": "You join in, make some friends and understand the topic better. (+2 KNOW, +1 SOC, -1 NRG)",
        },
        "on_failure": {
            "knowledge": -1,
            "social": 0,
            "energy": -1,
            "message": "You feel too awkward to join and leave confused. (-1 KNOW, -1 NRG)",
        },
    },
    {
        "id": "cafeteria_chat",
        "text": "In the mensa, a group is loudly discussing the exam topics.",
        "requirements": {"social": 2, "knowledge": 2},
        "on_success": {
            "knowledge": 1,
            "social": 1,
            "energy": 0,
            "message": "You join the discussion and clarify some concepts. (+1 KNOW, +1 SOC)",
        },
        "on_failure": {
            "knowledge": 0,
            "social": -1,
            "energy": 0,
            "message": "You try to join but cannot follow the discussion. (-1 SOC)",
        },
    },
    {
        "id": "all_nighter_talk",
        "text": "A friend suggests pulling an all-nighter together.",
        "requirements": {"energy": 3},
        "on_success": {
            "knowledge": 2,
            "social": 1,
            "energy": -2,
            "message": "You both push through and cover a lot of material. (+2 KNOW, +1 SOC, -2 NRG)",
        },
        "on_failure": {
            "knowledge": -1,
            "social": 0,
            "energy": -2,
            "message": "You are too tired, nothing sticks and you feel terrible. (-1 KNOW, -2 NRG)",
        },
    },
    {
        "id": "bully_event",
        "text": "A bully tries to steal your book in the hallway.",
        "requirements": {"energy": 3},
        "on_success": {
            "knowledge": 0,
            "social": 1,
            "energy": -1,
            "message": "You stand up to the bully and keep your book. (+1 SOC, -1 NRG)",
        },
        "on_failure": {
            "knowledge": -1,
            "social": -1,
            "energy": -2,
            "message": "The bully intimidates you and takes your book. (-1 KNOW, -1 SOC, -2 NRG)",
        },
    },
]


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 36)

        self.day = 1
        self.max_days = 5

        self.social = 0
        self.knowledge = 0
        self.energy = MAX_ENERGY

        self.phase = "morning"
        self.morning_actions_taken = 0
        self.selected = 0
        self.message = ""

        self.phase_backgrounds = {
            "morning": pygame.image.load("assets/images/phase_morning.png").convert(),
            "day": pygame.image.load("assets/images/phase_day.png").convert(),
            "evening": pygame.image.load("assets/images/phase_evening.png").convert(),
            "exam_pass": pygame.image.load("assets/images/phase_exam_pass.png").convert(),
            "exam_fail": pygame.image.load("assets/images/phase_exam_fail.png").convert(),
        }

        self.event_backgrounds = {
            "library_group": pygame.image.load("assets/images/event_library_group.png").convert(),
            "cafeteria_chat": pygame.image.load("assets/images/event_cafeteria_chat.png").convert(),
            "all_nighter_talk": pygame.image.load("assets/images/event_all_nighter_talk.png").convert(),
            "bully_event": pygame.image.load("assets/images/event_bully_event.png").convert(),
        }

        self.current_bg = self.phase_backgrounds["morning"]

    def update(self):
        pass

    def handle_event(self, event):
        if self.phase in ("exam", "game_over"):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.__init__(self.screen)
            return

        if event.type == pygame.KEYDOWN:
            options = self.get_options()
            if not options:
                return

            if event.key == pygame.K_UP:
                self.selected = max(0, self.selected - 1)
            elif event.key == pygame.K_DOWN:
                self.selected = min(len(options) - 1, self.selected + 1)
            elif event.key == pygame.K_RETURN:
                self.apply_choice(self.selected)

    def get_options(self):
        if self.phase == "morning":
            return [
                "Sleep in (+1 NRG)",
                "Check social media (+1 SOC)",
                "Make coffee (+1 NRG)",
                "Go over notes (+1 KNOW)",
            ]
        elif self.phase == "day":
            opts = ["Skip the day (go to evening)"]
            if self.energy >= 2:
                opts.append("Attend class (-2 NRG, +2 KNOW, extra -1 NRG from focus)")
            if self.energy >= 1:
                opts.append("Go to the library (-1 NRG, +1 KNOW)")
                opts.append("Hang out with friends (-1 NRG, +1 SOC)")
            return opts
        elif self.phase == "evening":
            return [
                "Study (+2 KNOW, -1 NRG)",
                "Socialize (+2 SOC, -1 NRG)",
                "Sleep early (+2 NRG)",
            ]
        return []

    def apply_choice(self, index):
        self.message = ""
        if self.phase == "morning":
            self.apply_morning_choice(index)
        elif self.phase == "day":
            self.apply_day_choice(index)
        elif self.phase == "evening":
            self.apply_evening_choice(index)
        self.clamp_stats()

    def apply_morning_choice(self, index):
        if index == 0:
            self.energy += 1
            self.message = "You slept in a bit."
        elif index == 1:
            self.social += 1
            self.message = "You scrolled through messages."
        elif index == 2:
            self.energy += 1
            self.message = "Coffee acquired."
        elif index == 3:
            self.knowledge += 1
            self.message = "You reviewed your notes."

        self.morning_actions_taken += 1
        if self.morning_actions_taken >= 2:
            self.phase = "day"
            self.selected = 0
            self.current_bg = self.phase_backgrounds["day"]
            self.trigger_random_event("morning_to_day")
            self.message += " Time to go to HFU."

    def apply_day_choice(self, index):
        options = self.get_options()
        label = options[index]
        moved_to_evening = False

        if label.startswith("Skip the day"):
            moved_to_evening = True
            self.message = "You took it easy today."
        elif "Attend class" in label and self.energy >= 2:
            self.energy -= 2
            self.knowledge += 2
            self.energy -= 1
            self.message = "You forced yourself through a boring lecture."
        elif "Go to the library" in label and self.energy >= 1:
            self.energy -= 1
            self.knowledge += 1
            self.message = "You studied quietly in the library."
        elif "Hang out with friends" in label and self.energy >= 1:
            self.energy -= 1
            self.social += 1
            self.message = "You had a good time with friends."

        if self.energy <= 0:
            self.energy = 0
            moved_to_evening = True
            self.message += " You are exhausted and head home."

        if moved_to_evening:
            self.phase = "evening"
            self.selected = 0
            self.current_bg = self.phase_backgrounds["evening"]
            self.trigger_random_event("day_to_evening")

    def apply_evening_choice(self, index):
        if index == 0:
            if self.energy >= 1:
                self.energy -= 1
                self.knowledge += 2
                self.message = "You studied in the evening."
            else:
                self.message = "You are too tired to study."
        elif index == 1:
            if self.energy >= 1:
                self.energy -= 1
                self.social += 2
                self.message = "You went out with friends."
            else:
                self.message = "You are too tired to go out."
        elif index == 2:
            self.energy += 2
            self.message = "You went to bed early."

        self.end_of_day()

    def trigger_random_event(self, transition_tag):
        event = random.choice(SKILL_EVENTS)
        event_id = event.get("id")
        bg = self.event_backgrounds.get(event_id)
        if bg is not None:
            self.current_bg = bg
        self.resolve_skill_event(event)

    def resolve_skill_event(self, event):
        text = event["text"]
        req = event.get("requirements", {})

        success = True
        if "social" in req and self.social < req["social"]:
            success = False
        if "knowledge" in req and self.knowledge < req["knowledge"]:
            success = False
        if "energy" in req and self.energy < req["energy"]:
            success = False

        if success:
            outcome = event["on_success"]
        else:
            outcome = event["on_failure"]

        self.social += outcome.get("social", 0)
        self.knowledge += outcome.get("knowledge", 0)
        self.energy += outcome.get("energy", 0)

        self.clamp_stats()
        self.message = text + " " + outcome["message"]

    def end_of_day(self):
        self.energy += 3
        if self.energy > MAX_ENERGY:
            self.energy = MAX_ENERGY

        self.day += 1
        self.morning_actions_taken = 0
        self.selected = 0

        if self.day > self.max_days:
            self.start_exam()
        else:
            self.phase = "morning"
            self.current_bg = self.phase_backgrounds["morning"]
            self.message += " New day."

    def start_exam(self):
        self.phase = "exam"
        if self.knowledge >= 10:
            self.current_bg = self.phase_backgrounds["exam_pass"]
            self.message = "Exam result: PASS. You survived the week at HFU. Press Enter to restart."
        else:
            self.current_bg = self.phase_backgrounds["exam_fail"]
            self.message = "Exam result: FAIL. Not enough knowledge. Press Enter to restart."
        self.selected = 0

    def clamp_stats(self):
        if self.energy > MAX_ENERGY:
            self.energy = MAX_ENERGY
        if self.energy < 0:
            self.energy = 0

    def draw_wrapped_text(self, text, x, y, max_width, color):
        if not text:
            return y

        words = text.split(" ")
        line = ""
        for word in words:
            test_line = line + (" " if line else "") + word
            width, _ = self.font.size(test_line)
            if width > max_width and line:
                surf = self.font.render(line, True, color)
                self.screen.blit(surf, (x, y))
                y += self.font.get_height() + 4
                line = word
            else:
                line = test_line

        if line:
            surf = self.font.render(line, True, color)
            self.screen.blit(surf, (x, y))
            y += self.font.get_height() + 4

        return y

    def draw(self):
        screen_w, screen_h = self.screen.get_size()

        panel_height = 260  # top UI area
        img_height = screen_h - panel_height

        # background (fallback)
        self.screen.fill((0, 0, 0))

        # draw stretched image under the panel (like your screenshot)
        if self.current_bg is not None:
            img_stretched = pygame.transform.scale(self.current_bg, (screen_w, img_height))
            self.screen.blit(img_stretched, (0, panel_height))

        # draw UI panel
        pygame.draw.rect(self.screen, (15, 15, 40), pygame.Rect(0, 0, screen_w, panel_height))

        header = "Day {}/{} - Phase: {}".format(
            self.day, self.max_days, self.phase.capitalize()
        )
        header_surf = self.big_font.render(header, True, (255, 255, 255))
        self.screen.blit(header_surf, (20, 10))

        stats = "SOC: {}  KNOW: {}  NRG: {}/{}".format(
            self.social, self.knowledge, self.energy, MAX_ENERGY
        )
        stats_surf = self.font.render(stats, True, (255, 255, 255))
        self.screen.blit(stats_surf, (20, 50))

        y = 90
        if self.message:
            y = self.draw_wrapped_text(self.message, 20, y, screen_w - 40, (255, 255, 0))
            # add spacing before options
            y += 5

        if self.phase in ("exam", "game_over"):
            return

        options = self.get_options()
        for i, label in enumerate(options):
            color = (255, 200, 200) if i == self.selected else (255, 255, 255)
            surf = self.font.render(label, True, color)
            self.screen.blit(surf, (40, y + i * 30))

