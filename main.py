import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((720, 600), pygame.RESIZABLE)
pygame.mouse.set_visible(False)
pygame.display.set_caption("Game Example")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
large_font = pygame.font.SysFont(None, 48)

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
CYAN = (173, 216, 230)
GREEN = (80, 200, 120)
RED = (200, 80, 80)
CHECK_GREEN = (50, 180, 70)

def safe_load(path, alpha=True, fallback_size=(80, 80), label=None):
    try:
        img = pygame.image.load(path)
        return img.convert_alpha() if alpha else img.convert()
    except Exception:
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill((200, 200, 200))
        if not label:
            label = path
        txt = pygame.font.SysFont(None, 18).render(label, True, BLACK)
        txt_r = txt.get_rect(center=(fallback_size[0]//2, fallback_size[1]//2))
        surf.blit(txt, txt_r)
        return surf

# === ALL YOUR ORIGINAL IMAGE LOADS (unchanged) ===
player_image = pygame.transform.smoothscale(safe_load("hand.png", label="hand"), (50, 65))

background1 = safe_load("background.png", alpha=False, fallback_size=screen.get_size(), label="bg1")
background2 = safe_load("background2.png", alpha=False, fallback_size=screen.get_size(), label="bg2")

banner1 = safe_load("banner1.png", label="banner1")
banner2 = safe_load("banner2.png", label="banner2")

start_img    = safe_load("start.png", label="start")
settings_img = safe_load("settings.png", label="settings")
quit_img     = safe_load("quit.png", label="quit")
yes_img      = safe_load("yes.png", label="yes")
no_img       = safe_load("no.png", label="no")

open_book   = safe_load("open_book.png", label="open_book")
closed_book = safe_load("closed_book.png", label="closed_book")
arrow_img   = safe_load("arrow.png", label="arrow")

adobo_img = safe_load("adobo.png", label="adobo")

choose_save_img = safe_load("choose_save.png", label="choose_save")
choose_dish_img = safe_load("choose_dish.png", label="choose_dish")

back_img = safe_load("back.png", label="back")
back_img = pygame.transform.smoothscale(back_img, (60, 60))
back_rect = back_img.get_rect(topleft=(20, 20))

options_icon = safe_load("settings_icon.png", label="opt")
hint_icon    = safe_load("hint_icon.png", label="hint")

options_icon = pygame.transform.smoothscale(options_icon, (80, 60))
hint_icon    = pygame.transform.smoothscale(hint_icon, (70, 60))

options_rect = options_icon.get_rect(topleft=(20, 20))
hint_rect    = hint_icon.get_rect(topright=(screen.get_width() - 20, 20))
options_icon_fade = options_icon.copy()
hint_icon_fade    = hint_icon.copy()

kitchen_popup2_img = safe_load("kitchen_popup2.png", label="popup2")
knife_img = safe_load("knife.png", label="knife")
guideline_img = safe_load("guideline.png", label="guideline")
potato_img = safe_load("potato.png", label="potato")
potato_origCut1_img = safe_load("potato_origCut1.png", label="potato_origCut1")
potato_origCut2_img = safe_load("potato_origCut2.png", label="potato_origCut2")
potato_cut4_img = safe_load("potato_cut4.png", label="potato_cut4")
potato_piece1 = safe_load("potato_cut1.png", label="potato_cut1")
potato_piece2 = safe_load("potato_cut2.png", label="potato_cut2")
potato_piece3 = safe_load("potato_cut3.png", label="potato_cut3")

kitchen_popup3_img = safe_load("kitchen_popup3.png", label="popup3")
kitchen_last_img     = safe_load("kitchen_last.png", alpha=False, label="kitchen_last")
stove_notOn_img      = safe_load("stove_notOn.png", label="stove_notOn")
stove_on_img         = safe_load("stove_on.png", label="stove_on")
pot_img              = safe_load("pot.png", label="pot")
pot_withoutLid_img   = safe_load("pot_withoutLid.png", label="pot_withoutLid")
bowl_marinate_img    = safe_load("bowl_marinate.png", label="bowl_marinate")
bowl_potato_img      = safe_load("bowl_potato.png", label="bowl_potato")

def scale_center(image, size, center):
    img = pygame.transform.smoothscale(image, size)
    rect = img.get_rect(center=center)
    return img, rect

adobo_img, adobo_rect = scale_center(adobo_img, (200, 200), (screen.get_width() // 2, screen.get_height() - 340))
adobo_base_y = adobo_y = adobo_rect.y

arrow_img, arrow_rect = scale_center(arrow_img, (60, 60), (screen.get_width() - 30, screen.get_height() // 2))

progress_value = 0.0

button_size = (180, 90)
start_img    = pygame.transform.smoothscale(start_img, button_size)
settings_img = pygame.transform.smoothscale(settings_img, button_size)
quit_img     = pygame.transform.smoothscale(quit_img, button_size)
yes_img      = pygame.transform.smoothscale(yes_img, (120, 60))
no_img       = pygame.transform.smoothscale(no_img, (120, 60))

background_timer   = 0
background_interval = 200
current_background = background1
current_banner     = banner1

fading       = False
fade_alpha   = 0
fade_speed   = 5

book_fade_alpha = 100
book_fade_speed = 5

confirming_slot       = None
show_confirmation     = False
book_open             = True
arrow_visible         = False
book_flipping         = False
book_flip_timer       = 0
book_flip_delay       = 1000
ui_hidden_permanently = False

header_alpha = 0
header_fade_speed = 6

dish_selected          = False
show_dish_confirmation = False
adobo_hovered          = False
adobo_jump_offset      = -10
fade_to_level          = False
level_fade_alpha       = 0

kitchen_loaded = False
kitchen_img = None
kitchen_fade_alpha = 0

arrow_base_y = arrow_rect.centery
arrow_current_y = arrow_base_y
arrow_jump_offset = -12

returning_to_file_selection = False

step1_completed = False

start_slice_transition = False
slice_fade_alpha = 0
slice_fade_speed = 6
slice_popup_visible = False
slice_setup_done = False
knife_static_rect = None
knife_is_cursor = False
slicing_holding = False
guideline_rect = None
guideline_points = []
guideline_visited = None
slice_count = 0
slice_piece_positions = []
slice_completed = False
slice_show_great = False
slice_setup_done = False
slice_completed = False
slice_count = 0
slice_piece_positions = []
guideline_visited = []
knife_is_cursor = False
slicing_holding = False
slice_state = {}

# Step 2 transition states
step2_arrow_visible = False
step2_fade_to_white = False
step2_fade_alpha = 0
step2_popup_ready = False
step2_completed = False

# Step 3
step3_fade_to_white = False
step3_fade_alpha = 0
step3_popup_visible = False
step3_setup_done = False
step3_completed = False
step3_fade_in_from_white = False
stove_on = False
pot_open = False
ingredients_in_pot = {"marinate": False, "potato": False}
cook_great_shown = False
cook_draggables = []
stove_rect = None
pot_rect = None
cook_success_text = False

class ImageButton:
    def __init__(self, image, callback):
        self.image = image
        self.callback = callback
        self.rect = self.image.get_rect()
        self.base_y = 0
        self.current_y = 0
        self.jump_offset = -10

    def update_position(self, center_x, y):
        self.base_y = y
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        target_y = self.base_y + (self.jump_offset if is_hovered else 0)
        self.current_y += (target_y - self.current_y) * 0.2
        self.rect.topleft = (center_x - self.rect.width // 2, int(self.current_y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()

class SaveSlot:
    def __init__(self, label, position):
        self.label = label
        self.rect = pygame.Rect(position[0], position[1], 200, 50)
        self.hovered = False
        self.alpha = 0

    def draw(self, surface, font):
        color = CYAN if self.hovered else GRAY
        slot_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        slot_surface.set_alpha(self.alpha)
        pygame.draw.rect(slot_surface, color, slot_surface.get_rect(), border_radius=10)
        pygame.draw.rect(slot_surface, BLACK, slot_surface.get_rect(), 2, border_radius=10)
        text = font.render(self.label, True, WHITE)
        text.set_alpha(self.alpha)
        text_rect = text.get_rect(center=slot_surface.get_rect().center)
        slot_surface.blit(text, text_rect)
        surface.blit(slot_surface, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

menu_active = True

def start_game():
    global fading
    fading = True

def show_credits():
    print("Game by Group 3")

def exit_game():
    pygame.quit()
    sys.exit()

def confirm_yes():
    global confirming_slot, show_confirmation, arrow_visible, fade_to_level, show_dish_confirmation
    if show_confirmation:
        print(f"{confirming_slot.label} confirmed")
        show_confirmation = False
        confirming_slot = None
        arrow_visible = True
    elif show_dish_confirmation:
        show_dish_confirmation = False
        fade_to_level = True

def confirm_no():
    global show_confirmation, confirming_slot, show_dish_confirmation
    show_confirmation = False
    confirming_slot = None
    show_dish_confirmation = False

buttons = [
    ImageButton(start_img, start_game),
    ImageButton(settings_img, show_credits),
    ImageButton(quit_img, exit_game)
]

save_slots = [
    SaveSlot("Save File 1", (screen.get_width() // 2 - 220, 170)),
    SaveSlot("Save File 2", (screen.get_width() // 2 - 220, 250)),
    SaveSlot("Save File 3", (screen.get_width() // 2 - 220, 330))
]

yes_button = ImageButton(yes_img, confirm_yes)
no_button = ImageButton(no_img, confirm_no)

current_screen = "main_menu"

marinate_setup_done = False

kitchen_popup_img = safe_load("kitchen_popup1.png", label="tutorial")

bowl_empty_img = safe_load("bowl_empty.png", label="bowl_empty")
bowl_marinate_img = safe_load("bowl_marinate.png", label="bowl_marinate")

img_bayleaf     = safe_load("bayleaf.png", label="bayleaf")
img_brown_sugar = safe_load("brown_sugar.png", label="brown_sugar")
img_garlic      = safe_load("garlic.png", label="garlic")
img_bowl_meat   = safe_load("bowl_meat.png", label="bowl_meat")
img_salt        = safe_load("salt.png", label="salt")
img_pepper      = safe_load("pepper.png", label="pepper")
img_soysauce    = safe_load("soysauce.png", label="soysauce")
img_vinegar     = safe_load("vinegar.png", label="vinegar")

class Draggable:
    def __init__(self, name, image, pos):
        self.name = name
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.dragging = False
        self.offset = (0,0)
        self.visible = True
        self.checked = False
        self.start_pos = pos

    def start_drag(self, mouse_pos):
        if not self.visible or self.checked:
            return False
        if self.rect.collidepoint(mouse_pos):
            self.dragging = True
            self.offset = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
            return True
        return False

    def stop_drag(self):
        self.dragging = False

    def update(self, mouse_pos):
        if self.dragging:
            self.rect.x = mouse_pos[0] - self.offset[0]
            self.rect.y = mouse_pos[1] - self.offset[1]

    def reset(self):
        self.rect.topleft = self.start_pos
        self.dragging = False

    def draw(self, surface):
        if self.visible and not self.checked:
            surface.blit(self.image, self.rect)

draggables = []

bowl_rect = None
bowl_current_image = bowl_empty_img

checklist_names = [
    "Salt", "Pepper", "Soysauce", "Vinegar",
    "Bayleaf", "Brownsugar", "Garlic", "Meat"
]
check_state = {name: False for name in checklist_names}

tutorial_popup_visible = False
tutorial_shown = False

marinate_completed = False
show_great_job = False
great_job_timer = 0

continue_arrow_rect = pygame.Rect(0,0,50,30)

arrow_clicked = False  # reset at start of frame
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if continue_arrow_rect.collidepoint(event.pos):
            arrow_clicked = True

running = True
dt = 0
while running:
    if menu_active:
        background_timer += dt * 1000
        if background_timer >= background_interval:
            background_timer = 0
            current_background = background2 if current_background == background1 else background1
            current_banner = banner2 if current_banner == banner1 else banner1
        screen.blit(pygame.transform.scale(current_background, screen.get_size()), (0, 0))
    else:
        screen.fill(WHITE)

    if not menu_active and not dish_selected:
        if book_fade_alpha < 255:
            book_fade_alpha += book_fade_speed
        for slot in save_slots:
            slot.alpha = book_fade_alpha

        book_image = open_book if book_open else closed_book
        book_width = 760
        book_height = book_width * book_image.get_height() // book_image.get_width()
        book_scaled = pygame.transform.smoothscale(book_image, (book_width, book_height))
        faded_book = book_scaled.copy()
        faded_book.set_alpha(book_fade_alpha)
        book_rect = faded_book.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(faded_book, book_rect)

        if not ui_hidden_permanently:
            choose_save_scaled = pygame.transform.smoothscale(choose_save_img, (350, 80))
            header_surface = choose_save_scaled.copy()
            header_surface.set_alpha(header_alpha)
            header_rect = header_surface.get_rect(center=(screen.get_width() // 2, 90))
            screen.blit(header_surface, header_rect)
        elif not dish_selected and not book_flipping and book_open and ui_hidden_permanently:
            choose_dish_scaled = pygame.transform.smoothscale(choose_dish_img, (350, 130))
            header_surface = choose_dish_scaled.copy()
            header_surface.set_alpha(header_alpha)
            header_rect = header_surface.get_rect(center=(screen.get_width() // 2, 90))
            screen.blit(header_surface, header_rect)

        if current_screen in ["file_selection", "dish_selection"]:
            screen.blit(back_img, back_rect)

        if not dish_selected and not book_flipping and book_open and ui_hidden_permanently:
            mouse_pos = pygame.mouse.get_pos()
            adobo_hovered = adobo_rect.collidepoint(mouse_pos)
            target_y = adobo_base_y + (adobo_jump_offset if adobo_hovered else 0)
            adobo_y += (target_y - adobo_y) * 0.2
            adobo_rect.y = int(adobo_y)
            screen.blit(adobo_img, adobo_rect)

        if show_dish_confirmation:
            prompt_text = font.render("Cook the adobo?", True, GRAY)
            prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
            screen.blit(prompt_text, prompt_rect)
            yes_button.update_position (screen.get_width() // 2 - 80, screen.get_height() - 65)
            no_button.update_position (screen.get_width() // 2 + 80, screen.get_height() - 65)
            yes_button.draw(screen)
            no_button.draw(screen)

        mouse_pos = pygame.mouse.get_pos()
        if not ui_hidden_permanently:
            for slot in save_slots:
                slot.check_hover(mouse_pos)
                slot.draw(screen, font)

        if show_confirmation and confirming_slot:
            prompt_text = font.render("Use this save file?", True, GRAY)
            prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
            screen.blit(prompt_text, prompt_rect)
            yes_button.update_position (screen.get_width() // 2 - 80, screen.get_height() - 65)
            no_button.update_position (screen.get_width() // 2 + 80, screen.get_height() - 65)
            yes_button.draw(screen)
            no_button.draw(screen)

        if arrow_visible:
            arrow_rect.right = screen.get_width() - 60
            arrow_base_y = screen.get_height() // 2

            mouse_pos = pygame.mouse.get_pos()
            hovered = arrow_rect.collidepoint(mouse_pos)

            target_y = arrow_base_y + (arrow_jump_offset if hovered else 0)
            arrow_current_y += (target_y - arrow_current_y) * 0.2

            arrow_rect.centery = int(arrow_current_y)

            screen.blit(arrow_img, arrow_rect)

    if not ui_hidden_permanently:
        if header_alpha < 255:
            header_alpha += header_fade_speed
    elif ui_hidden_permanently and not dish_selected and book_open:
        if header_alpha < 255:
            header_alpha += header_fade_speed

    if book_flipping:
        current_time = pygame.time.get_ticks()
        if current_time - book_flip_timer >= book_flip_delay:
            book_open = True
            book_flipping = False

            if returning_to_file_selection:
                current_screen = "file_selection"
                ui_hidden_permanently = False
                header_alpha = 0
                returning_to_file_selection = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if menu_active and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in buttons:
                button.check_click(event.pos)

        if not menu_active and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if back_rect.collidepoint(event.pos):
                if current_screen == "dish_selection" and not book_flipping:
                    book_open = False
                    book_flipping = True
                    book_flip_timer = pygame.time.get_ticks()
                    returning_to_file_selection = True
                elif current_screen == "file_selection":
                    current_screen = "main_menu"
                    menu_active = True
                    ui_hidden_permanently = False
                    header_alpha = 0

            if show_confirmation:
                yes_button.check_click(event.pos)
                no_button.check_click(event.pos)
            elif not ui_hidden_permanently:
                for slot in save_slots:
                    if slot.check_click(event.pos):
                        confirming_slot = slot
                        show_confirmation = True
            if arrow_visible and not ui_hidden_permanently:
                if arrow_rect.collidepoint(event.pos) and not book_flipping:
                    if marinate_completed:
                        start_slice_transition = True
                        arrow_visible = False
                        step1_completed = True
                    else:
                        book_open = False
                        book_flipping = True
                        book_flip_timer = pygame.time.get_ticks()
                        arrow_visible = False
                        ui_hidden_permanently = True
                        current_screen = "dish_selection"

        if not menu_active and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if show_confirmation:
                yes_button.check_click(event.pos)
                no_button.check_click(event.pos)
            elif show_dish_confirmation:
                yes_button.check_click(event.pos)
                no_button.check_click(event.pos)
            elif not ui_hidden_permanently:
                for slot in save_slots:
                    if slot.check_click(event.pos):
                        confirming_slot = slot
                        show_confirmation = True
                if arrow_visible and arrow_rect.collidepoint(event.pos) and not book_flipping and not step1_completed:
                    book_open = False
                    book_flipping = True
                    book_flip_timer = pygame.time.get_ticks()
                    arrow_visible = False
                    ui_hidden_permanently = True
            elif not dish_selected and adobo_rect.collidepoint(event.pos):
                show_dish_confirmation = True

        if dish_selected and kitchen_loaded:
            if tutorial_popup_visible:
                popup_w = min(600, screen.get_width() - 100)
                popup_h = min(400, screen.get_height() - 120)
                popup_img_scaled = pygame.transform.smoothscale(kitchen_popup_img, (popup_w, popup_h))
                popup_rect = popup_img_scaled.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                close_rect = pygame.Rect(popup_rect.right - 44, popup_rect.top + 8, 36, 36)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if close_rect.collidepoint(event.pos):
                        tutorial_popup_visible = False
                        tutorial_shown = True
                if tutorial_popup_visible:
                    continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for d in draggables:
                    if d.start_drag(event.pos):
                        break

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for d in draggables:
                    if d.dragging:
                        d.stop_drag()
                        if bowl_rect and d.visible and not d.checked and d.rect.colliderect(bowl_rect):
                            d.checked = True
                            d.visible = False
                            if d.name in check_state:
                                check_state[d.name] = True
                        else:
                            d.reset()

            if event.type == pygame.MOUSEMOTION:
                for d in draggables:
                    d.update(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if arrow_visible and arrow_rect.collidepoint(event.pos) and not book_flipping:
                if marinate_completed and not step1_completed:
                    start_slice_transition = True
                    arrow_visible = False
                    step1_completed = True
                    step2_fade_to_white = True
                    step2_fade_alpha = 0
                    ui_hidden_permanently = True
                    show_great_job = False
                    bowl_rect = None

    if step1_completed:
        if start_slice_transition:
            pass

        if slice_popup_visible:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                popup_w = min(600, screen.get_width() - 100)
                popup_h = min(400, screen.get_height() - 120)
                pop_img = pygame.transform.smoothscale(kitchen_popup2_img, (popup_w, popup_h))
                pop_rect = pop_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                close_r = pygame.Rect(pop_rect.right - 44, pop_rect.top + 8, 36, 36)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if close_r.collidepoint(event.pos):
                        slice_popup_visible = False
                        slice_setup_done = False

        if slice_setup_done and not knife_is_cursor:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if knife_static_rect and knife_static_rect.collidepoint(event.pos):
                    knife_is_cursor = True
                    slicing_holding = True
        if knife_is_cursor:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                slicing_holding = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                slicing_holding = False

        if marinate_completed and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if continue_arrow_rect.collidepoint(event.pos):
                start_slice_transition = True
                slice_popup_visible = False
                slice_setup_done = False
                arrow_visible = False
        if slice_completed and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            gj_text = large_font.render("Great Job!", True, WHITE)
            gj_r = gj_text.get_rect(center=(screen.get_width()//2, options_rect.centery + 10))
            screen.blit(gj_text, gj_r)

            arrow_img, arrow_rect = scale_center(arrow_img, (60, 60), (gj_r.centerx + 120, gj_r.bottom + 20))
            screen.blit(arrow_img, arrow_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if arrow_rect.collidepoint(event.pos):
                        step3_fade_to_white = True
                        step2_completed = True
                        arrow_visible = False
                        slice_show_great = False
                        
        if step3_fade_in_from_white:
            kitchen_scaled = pygame.transform.scale(kitchen_img, screen.get_size())
            screen.blit(kitchen_scaled, (0, 0))

            step3_fade_alpha -= 8
            fade_surf = pygame.Surface(screen.get_size())
            fade_surf.fill(WHITE)
            fade_surf.set_alpha(max(0, step3_fade_alpha))
            screen.blit(fade_surf, (0, 0))

            if step3_fade_alpha <= 0:
                step3_fade_in_from_white = False
                step3_fade_alpha = 0
                kitchen_fade_alpha = 255 # Ensure UI icons are fully visible

    if menu_active:
        banner_x = screen.get_width() // 2
        center_x = screen.get_width() // 4
        start_y = screen.get_height() // 2 - 40
        spacing = 80

        banner_width = 280
        banner_height = banner_width * current_banner.get_height() // current_banner.get_width()
        banner_scaled = pygame.transform.smoothscale(current_banner, (banner_width, banner_height))
        banner_rect = banner_scaled.get_rect(center=(banner_x, screen.get_height() // 5.5))
        screen.blit(banner_scaled, banner_rect)

        for i, button in enumerate(buttons):
            button.update_position(center_x, start_y + i * spacing)
            button.draw(screen)

    if fading:
        fade_alpha += fade_speed
        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill(WHITE)
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        if fade_alpha >= 255:
            fading = False
            menu_active = False
            fade_alpha = 0
            current_screen = "file_selection"

    if fade_to_level:
        level_fade_alpha += fade_speed
        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill(WHITE)
        fade_surface.set_alpha(level_fade_alpha)
        screen.blit(fade_surface, (0, 0))
        if level_fade_alpha >= 255:
            fade_to_level = False
            level_fade_alpha = 0
            dish_selected = True
            try:
                kitchen_img = safe_load("kitchen.png", alpha=False, label="kitchen")
                kitchen_loaded = True
            except Exception:
                print("Error: 'kitchen.png' not found or failed to load.")

    if start_slice_transition:
        slice_fade_alpha += slice_fade_speed
        f = pygame.Surface(screen.get_size())
        f.fill(WHITE)
        f.set_alpha(min(255, int(slice_fade_alpha)))
        screen.blit(f, (0, 0))
        if slice_fade_alpha >= 255:
            start_slice_transition = False
            slice_fade_alpha = 0
            slice_popup_visible = True
            dish_selected = True
            try:
                kitchen_img = safe_load("kitchen.png", alpha=False, label="kitchen")
                kitchen_loaded = True
            except Exception:
                kitchen_loaded = False


    if dish_selected and kitchen_loaded:
        kitchen_scaled = pygame.transform.scale(kitchen_img, screen.get_size())
        kitchen_fade = kitchen_scaled.copy()
        if kitchen_fade_alpha < 255:
            kitchen_fade_alpha += fade_speed
        kitchen_fade.set_alpha(kitchen_fade_alpha)
        screen.blit(kitchen_fade, (0, 0))

        options_icon_fade.set_alpha(kitchen_fade_alpha)
        hint_icon_fade.set_alpha(kitchen_fade_alpha)

        options_rect.topleft = (20, 20)
        hint_rect.topright   = (screen.get_width() - 20, 20)

        screen.blit(options_icon_fade, options_rect)
        screen.blit(hint_icon_fade, hint_rect)

        if kitchen_fade_alpha >= 250 and not marinate_setup_done and not slice_popup_visible and not start_slice_transition:
            bowl_w = min(260, screen.get_width() // 3)
            bowl_h = int(bowl_w * bowl_empty_img.get_height() / (bowl_empty_img.get_width() or 1))
            bowl_current_image = pygame.transform.smoothscale(bowl_empty_img, (bowl_w, bowl_h))
            bowl_rect = bowl_current_image.get_rect(center=(screen.get_width() // 2, int(screen.get_height() * 0.7)))

            row1_y = screen.get_height() - 130
            row2_y = screen.get_height() - 90

            row1_offset_x = screen.get_width() // 2 - 350
            row2_offset_x = screen.get_width() // 2 + 20
            spacing_x = 90

            row1 = [
                ("Salt", img_salt),
                ("Soysauce", img_soysauce),
                ("Pepper", img_pepper),
                ("Vinegar", img_vinegar),
            ]

            row2 = [
                ("Bayleaf", img_bayleaf),
                ("Meat", img_bowl_meat),
                ("Brownsugar", img_brown_sugar),
                ("Garlic", img_garlic),
            ]

            def scaled(img):
                w = 70
                h = int(w * img.get_height() / (img.get_width() or 1))
                return pygame.transform.smoothscale(img, (w, h))

            draggables.clear()

            for i, (name, img) in enumerate(row1):
                s = scaled(img)
                pos = (row1_offset_x + i * spacing_x, row1_y)
                draggables.append(Draggable(name, s, pos))

            for i, (name, img) in enumerate(row2):
                s = scaled(img)
                pos = (row2_offset_x + i * spacing_x, row2_y)
                draggables.append(Draggable(name, s, pos))

            for k in check_state:
                check_state[k] = False

            marinate_setup_done = True
            tutorial_popup_visible = True

        if bowl_rect:
            screen.blit(bowl_current_image, bowl_rect)

        for d in draggables:
            d.draw(screen)

        if bowl_rect:
            checklist_x = bowl_rect.centerx
            checklist_y = bowl_rect.top - 80
            per_row = 4
            box_w = 120
            box_h = 32
            gap = 14
            title = font.render("Marinate Checklist", True, WHITE)
            trect = title.get_rect(center=(checklist_x, checklist_y - 60))
            screen.blit(title, trect)
            for idx, name in enumerate(checklist_names):
                row = idx // per_row
                col = idx % per_row
                x = checklist_x - ((per_row * box_w + (per_row - 1) * gap) // 2) + col * (box_w + gap)
                y = checklist_y + row * (box_h + 8)
                rect = pygame.Rect(x, y, box_w, box_h)
                pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
                if check_state.get(name, False):
                    pygame.draw.rect(screen, CHECK_GREEN, rect.inflate(-4, -4), border_radius=6)
                    txt = font.render(name, True, WHITE)
                else:
                    pygame.draw.rect(screen, GRAY, rect.inflate(-4, -4), border_radius=6)
                    txt = font.render(name, True, WHITE)
                txt_r = txt.get_rect(center=rect.center)
                screen.blit(txt, txt_r)

        if not marinate_completed and all(check_state.values()) and marinate_setup_done:
            marinate_completed = True
            try:
                bowl_m = pygame.transform.smoothscale(bowl_marinate_img, (bowl_rect.width, bowl_rect.height))
                bowl_current_image = bowl_m
            except Exception:
                pass
            show_great_job = True
            great_job_timer = pygame.time.get_ticks()
            arrow_visible = True

        if show_great_job and not slice_popup_visible and not start_slice_transition:
            gj_text = large_font.render("Great Job!", True, WHITE)
            gj_r = gj_text.get_rect(center=(screen.get_width()//2, options_rect.centery + 10))
            screen.blit(gj_text, gj_r)
            arrow_img, arrow_rect = scale_center(arrow_img, (60, 60), (gj_r.centerx + 120, gj_r.bottom + 20))
            screen.blit(arrow_img, arrow_rect)

        if step2_fade_to_white:
            step2_fade_alpha += fade_speed
            fade_surface = pygame.Surface(screen.get_size())
            fade_surface.fill(WHITE)
            fade_surface.set_alpha(min(255, int(step2_fade_alpha)))
            screen.blit(fade_surface, (0, 0))

            if step2_fade_alpha >= 255:
                step2_fade_to_white = False
                step2_popup_ready = True 

        if tutorial_popup_visible:
            popup_w = min(600, screen.get_width() - 100)
            popup_h = min(400, screen.get_height() - 120)
            popup_img_scaled = pygame.transform.smoothscale(kitchen_popup_img, (popup_w, popup_h))
            popup_rect = popup_img_scaled.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            back = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            back.fill((10, 10, 10, 150))
            screen.blit(back, (0,0))
            screen.blit(popup_img_scaled, popup_rect)
            close_rect = pygame.Rect(popup_rect.right - 44, popup_rect.top + 8, 36, 36)
            pygame.draw.ellipse(screen, RED, close_rect)
            x_txt = font.render("X", True, WHITE)
            xt_r = x_txt.get_rect(center=close_rect.center)
            screen.blit(x_txt, xt_r)
            helper = font.render("Click X to start Step 1: Marinate", True, BLACK)
            helper_r = helper.get_rect(center=(popup_rect.centerx, popup_rect.bottom - 40))
            screen.blit(helper, helper_r)

        if slice_popup_visible:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if close_rect.collidepoint(event.pos):
                        step2_popup_ready = False
                        slice_popup_visible = True  # or slice_setup_done = True
            popup_w = min(600, screen.get_width() - 100)
            popup_h = min(400, screen.get_height() - 120)
            popup_img_scaled = pygame.transform.smoothscale(kitchen_popup2_img, (popup_w, popup_h))
            popup_rect = popup_img_scaled.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            back = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            back.fill((10, 10, 10, 150))
            screen.blit(back, (0,0))
            screen.blit(popup_img_scaled, popup_rect)
            close_rect = pygame.Rect(popup_rect.right - 44, popup_rect.top + 8, 36, 36)
            pygame.draw.ellipse(screen, RED, close_rect)
            x_txt = font.render("X", True, WHITE)
            xtr = x_txt.get_rect(center=close_rect.center)
            screen.blit(x_txt, xtr)
            helper = font.render("Click X to start Step 2: Slice", True, BLACK)
            helper_r = helper.get_rect(center=(popup_rect.centerx, popup_rect.bottom - 40))
            screen.blit(helper, helper_r)
        else:
            if step1_completed and not slice_setup_done and not slice_popup_visible and kitchen_fade_alpha >= 250:
                potato_w = min(100, int(screen.get_width() * 0.32))
                potato_h = int(potato_w * potato_img.get_height() / (potato_img.get_width() or 1))
                potato_scaled = pygame.transform.smoothscale(potato_img, (potato_w, potato_h))
                potato_rect = potato_scaled.get_rect(midbottom=(screen.get_width()//2, int(screen.get_height()*0.85)))
                guide_w = 35
                guide_h = 180
                guide_scaled = pygame.transform.smoothscale(guideline_img, (guide_w, guide_h))
                guideline_rect = guide_scaled.get_rect(center=potato_rect.center)

                knife_w = 100
                knife_h = int(knife_w * knife_img.get_height() / (knife_img.get_width() or 1))
                knife_scaled = pygame.transform.smoothscale(knife_img, (knife_w, knife_h))
                knife_static_rect = knife_scaled.get_rect(center=(screen.get_width()//2 + 200, 300))

                guideline_points = []
                N = 12
                step = max(1, (guide_scaled.get_width() - 20) // (N - 1))
                for i in range(N):
                    px = guideline_rect.left + 10 + i * step
                    py = guideline_rect.centery
                    guideline_points.append((px, py))
                guideline_visited = [False] * len(guideline_points)

                slice_piece_positions = []
                for i in range(3):
                    sx = potato_rect.right + 50 + i * (potato_w // 3)
                    sy = potato_rect.bottom - 50 
                    slice_piece_positions.append((sx, sy))

                slice_count = 0
                slice_completed = False
                slice_show_great = False
                knife_is_cursor = False
                slicing_holding = False
                slice_setup_done = True

                slice_state = {
                    "potato_scaled": potato_scaled,
                    "potato_rect": potato_rect,
                    "guide_scaled": guide_scaled,
                    "knife_scaled": knife_scaled
                }
    
            if slice_setup_done and not step2_fade_to_white and not step3_fade_in_from_white:
                potato_scaled = slice_state["potato_scaled"]
                potato_rect = slice_state["potato_rect"]
                guide_scaled = slice_state["guide_scaled"]
                knife_scaled = slice_state["knife_scaled"]
                screen.blit(potato_scaled, potato_rect)

                gs = guide_scaled.copy()
                gs.set_alpha(200)
                screen.blit(gs, guideline_rect)

                if not knife_is_cursor:
                    screen.blit(knife_scaled, knife_static_rect)

                for idx, (px, py) in enumerate(guideline_points):
                    color = (0,200,0) if guideline_visited[idx] else (200,80,80)
                    pygame.draw.circle(screen, color, (int(px), int(py)), 6)

                if knife_is_cursor:
                    mx, my = pygame.mouse.get_pos()
                    krect = knife_scaled.get_rect(center=(mx, my))
                    screen.blit(knife_scaled, krect)

                if knife_is_cursor and slicing_holding:
                    mx, my = pygame.mouse.get_pos()
                    for i, (px, py) in enumerate(guideline_points):
                        if not guideline_visited[i]:
                            dx = mx - px
                            dy = my - py
                            if (dx*dx + dy*dy) <= (20*20):
                                guideline_visited[i] = True

                if all(guideline_visited) and slice_count < 3:
                    slice_count += 1
                    if slice_count == 1:
                        try:
                            slice1 = pygame.transform.smoothscale(potato_piece1, (potato_w, potato_h))
                        except:
                            slice1 = potato_piece1
                        try:
                            slice_state["potato_scaled"] = pygame.transform.smoothscale(potato_origCut1_img, (potato_w, potato_h))
                        except:
                            pass
                    elif slice_count == 2:
                        try:
                            slice2 = pygame.transform.smoothscale(potato_piece2, (potato_w, potato_h))
                        except:
                            slice2 = potato_piece2
                        try:
                            slice_state["potato_scaled"] = pygame.transform.smoothscale(potato_origCut2_img, (potato_w, potato_h))
                        except:
                            pass
                    elif slice_count == 3:
                        try:
                            slice3 = pygame.transform.smoothscale(potato_piece3, (potato_w, potato_h))
                        except:
                            slice3 = potato_piece3
                        try:
                            slice_state["potato_scaled"] = pygame.transform.smoothscale(potato_cut4_img, (potato_w, potato_h))
                        except:
                            pass

                    guideline_visited = [False] * len(guideline_points)
                    knife_is_cursor = False
                    slicing_holding = False

                    if slice_count == 1:
                        piece1_surf = slice1
                    elif slice_count == 2:
                        piece2_surf = slice2
                    elif slice_count == 3:
                        piece3_surf = slice3

                if slice_count >= 1:
                    try:
                        screen.blit(piece1_surf, slice_piece_positions[0])
                    except:
                        pass
                if slice_count >= 2:
                    try:
                        screen.blit(piece2_surf, slice_piece_positions[1])
                    except:
                        pass
                if slice_count >= 3:
                    try:
                        screen.blit(piece3_surf, slice_piece_positions[2])
                    except:
                        pass

                if slice_count >= 3 and not slice_show_great:
                    slice_show_great = True
                    slice_completed = True
                if slice_show_great and step2_completed == False:
                    gj_text = large_font.render("Great Job!", True, WHITE)
                    gj_r = gj_text.get_rect(center=(screen.get_width()//2, options_rect.centery + 10))
                    screen.blit(gj_text, gj_r)

                    arrow_img_scaled, step2_arrow_rect = scale_center(arrow_img, (60, 60), (gj_r.centerx + 120, gj_r.bottom + 20))
                    screen.blit(arrow_img_scaled, step2_arrow_rect)

                    # Detect click on arrow
                    mouse_pos = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0] and step2_arrow_rect.collidepoint(mouse_pos):
                        step2_fade_to_white = True
                        slice_show_great = False
                        arrow_visible = False
                        step2_fade_alpha = 0

                        # HIDE all step 2 UI elements
                        slice_setup_done = False
                        slice_completed = False
                        slice_count = 0
                        slice_piece_positions = []
                        guideline_visited = []
                        knife_is_cursor = False
                        slicing_holding = False
                        slice_state = {}

                # Fade to white
                if step2_fade_to_white:
                    step2_fade_alpha += fade_speed
                    fade_surf = pygame.Surface(screen.get_size())
                    fade_surf.fill(WHITE)
                    fade_surf.set_alpha(min(255, int(step2_fade_alpha)))
                    screen.blit(fade_surf, (0, 0))

                    if step2_fade_alpha >= 255:
                        step2_fade_to_white = False
                        step2_fade_in_from_white = True
                        kitchen_img = kitchen_last_img  # switch background to last kitchen
                        step2_fade_alpha = 255

                # Fade back from white to kitchen_last.png
                if 'step2_fade_in_from_white' in globals() and step2_fade_in_from_white:
                    kitchen_scaled = pygame.transform.scale(kitchen_img, screen.get_size())
                    screen.blit(kitchen_scaled, (0, 0))

                    step2_fade_alpha -= fade_speed
                    fade_surf = pygame.Surface(screen.get_size())
                    fade_surf.fill(WHITE)
                    fade_surf.set_alpha(max(0, step2_fade_alpha))
                    screen.blit(fade_surf, (0, 0))

                    if step2_fade_alpha <= 0:
                        step2_fade_in_from_white = False
                        step2_fade_alpha = 0
                        kitchen_fade_alpha = 255  # ensure UI icons fully visible

                if step3_fade_to_white:
                    step3_fade_alpha += 8
                    fade_surf = pygame.Surface(screen.get_size())
                    fade_surf.fill(WHITE)
                    fade_surf.set_alpha(min(255, step3_fade_alpha))
                    screen.blit(fade_surf, (0, 0))
                    if step3_fade_alpha >= 255:
                        step3_fade_to_white = False
                        step3_fade_alpha = 255
                        step3_fade_in_from_white = True
                        step3_popup_visible = True
                        kitchen_img = kitchen_last_img  # switch background
                        kitchen_loaded = True
                                
        mouse_pos = pygame.mouse.get_pos()
        if options_rect.collidepoint(mouse_pos):
            pass

    mouse_pos = pygame.mouse.get_pos()
    if not (slice_setup_done and knife_is_cursor):
        image_rect = player_image.get_rect(center=mouse_pos)
        screen.blit(player_image, image_rect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
