"""
CSSE1001 Semester 2, 2018
UNO++ GUI Support Code
"""

import tkinter as tk
from tkinter import messagebox

from a2 import HumanPlayer, ComputerPlayer, Deck
from a2 import SkipCard, ReverseCard, Pickup2Card, Pickup4Card
from a2_support import FULL_DECK, build_deck, UnoGame, generate_name

__version__ = "1.0.1"


CARD_HEIGHT = 100
CARD_WIDTH = 75
CARD_SPACE = 10

CARD_OVAL_COLOUR = "#fceee3"
CARD_BACK_BACKGROUND = "black"
CARD_BACK_FOREGROUND = "red"
CARD_BACK_TEXT_COLOUR = "yellow"
CARD_BACK_TEXT = "UNO++"

AI_DELAY = 2000


class CardView:
    """
    A class to manage the drawing of a Uno card on a canvas.
    """

    def __init__(self, canvas, left_side, oval_colour=CARD_OVAL_COLOUR,
                 background_colour=CARD_BACK_BACKGROUND,
                 foreground_colour=CARD_BACK_FOREGROUND,
                 text_colour=CARD_BACK_TEXT_COLOUR, text=CARD_BACK_TEXT):
        """
        Construct a new card to be drawn on the given canvas at the left_position.

        Parameters:
            canvas (tk.Canvas): The canvas to draw the card onto.
            left_side (int): The amount of pixels in the canvas to draw the card.
            oval_colour (tk.Color): Colour of the oval for this card.
            background_colour (tk.Color): Backface card background colour.
            foreground_colour (tk.Color): Backface card foreground colour.
            text_colour (tk.Color): Backface card text colour.
            text (str): Backface card text to display.
        """
        self._canvas = canvas

        self.left_side = left_side
        self.right_side = left_side + CARD_WIDTH

        self._oval_colour = oval_colour
        self._background = background_colour
        self._foreground = foreground_colour
        self._text_colour = text_colour
        self._text = text
        self._image = None

        self.draw()

    def draw(self):
        """Draw the backface of the card to the canvas."""
        self._back = self.draw_back(self._background)
        self._oval = self.draw_circle(self._foreground)
        self._text_view = self.draw_text(self._text, self._text_colour)

    def redraw(self, card):
        """Redraw the card view with the properties of the given card.

        Parameters:
            card (Card): The card to draw to the canvas. If None, draw the
                         backface of the card.
        """
        if card is not None:
            print(card)
            # draw the card with details from the card parameter
            self._canvas.itemconfig(self._back, fill=card.get_colour().value)
            self._canvas.itemconfig(self._oval, fill=self._oval_colour)
            self._canvas.itemconfig(self._text_view, fill=card.get_colour().value,
                                    text=card.get_number())
        else:
            # draw the backface of the card
            self._canvas.itemconfig(self._back, fill=self._background)
            self._canvas.itemconfig(self._oval, fill=self._foreground)
            self._canvas.itemconfig(self._text_view, fill=self._text_colour,
                                    text=self._text)

    def draw_back(self, colour):
        """Draw the back of the canvas (the background not the backface).

        Parameters:
            colour (tk.Color): The colour of the background.
        """
        return self._canvas.create_rectangle(self.left_side, 0,
                                             self.right_side, CARD_HEIGHT,
                                             fill=colour)

    def draw_circle(self, colour):
        """Draw a circle in the middle of the card.

        Parameters:
            colour (tk.Color): The colour of the cirlce.
        """
        return self._canvas.create_oval(self.left_side + 10, 10,
                                        self.right_side - 10, CARD_HEIGHT - 10,
                                        fill=colour)

    def draw_text(self, text, colour):
        """Draw text in the middle of the card.

        Parameters:
            text (str): The text to display on the card.
            colour (tk.Color): The colour of the text to display.
        """
        return self._canvas.create_text(self.left_side + (CARD_WIDTH // 2),
                                        CARD_HEIGHT // 2, text=text, fill=colour,
                                        font=('Times', '16', 'bold italic'))

    def draw_image(self, image):
        """Draw an image in the middle of the card.

        Parameters:
            image (str): The filepath of the image to display.
        """
        self._image = tk.PhotoImage(file=image)
        return self._canvas.create_image(self.left_side + (CARD_WIDTH // 2),
                                         CARD_HEIGHT // 2, image=self._image)


CARD_ICONS = {
    SkipCard: "skip",
    ReverseCard: "reverse"
}


class IconCardView(CardView):
    """
    A card that has an image associated with it.
    """

    def draw(self):
        """Draw the backface of the card to the canvas."""
        super().draw()
        self._image_view = None

    def redraw(self, card):
        """Redraw the card view with an icon.

        Parameters:
            card (Card): The card to draw to the canvas. If None, draw the
                         backface of the card.
        """
        super().redraw(card)

        if card is not None:
            # clear text on the card
            self._canvas.itemconfig(self._text_view, text="")

            if self._image_view is None:
                # draw an image based on the card's class
                image = CARD_ICONS.get(card.__class__, "skip")
                #self._image_view = self.draw_image(f"images/{image}.png")
                self._image_view = self.draw_text(image, 'black')
            else:
                # show the image
                self._canvas.itemconfig(self._image_view, state="normal")
        else:
            if self._image_view is not None:
                # hide the image
                self._canvas.itemconfig(self._image_view, state="hidden")


class PickupCardView(CardView):
    """
    A card that displays the amount of cards to pickup.
    """

    def redraw(self, card):
        """Redraw the card view with the properties of the given card.

        Parameters:
            card (Card): The card to draw to the canvas. If None, draw the
                         backface of the card.
        """
        super().redraw(card)

        if card is not None:
            self._canvas.itemconfig(self._text_view,
                                    text=f"+{card.get_pickup_amount()}")


CARD_VIEWS = {
    SkipCard: IconCardView,
    ReverseCard: IconCardView,
    Pickup2Card: PickupCardView,
    Pickup4Card: PickupCardView
}


class DeckView(tk.Canvas):
    """
    A Canvas that displays a deck of uno cards on a board.
    """

    def __init__(self, master, pick_card=None, border_colour="#6D4C41",
                 active_border="red", offset=CARD_WIDTH, *args, **kwargs):
        """
        Construct a deck view.

        Parameters:
            master (tk.Tk|tk.Frame): The parent of this canvas.
            pick_card (callable): The callback when card in this deck is clicked.
                                  Takes an int representing the cards index.
            border_colour (tk.Color): The colour of the decks border.
            offset (int): The offset between cards in the deck.
        """
        super().__init__(master, *args, **kwargs, bg=border_colour,
                         highlightthickness=5, highlightbackground=border_colour)

        self._active = False
        self._playing = False

        self.offset = offset
        self.pick_card = pick_card
        self.cards = {}

        self._border_colour = border_colour
        self._active_border = active_border

        self.bind("<Button-1>", self._handle_click)

    def toggle_active(self, active=None):
        """Toggle whether the deck should be clickable.

        Parameters:
            active (bool): Whether to activate the deck.
        """
        if active is None:
            self._active = not self._active
        else:
            self._active = active

    def toggle_playing(self, playing=None):
        """Toggle whether the deck is the deck being played.

        Parameters:
            playing (bool): Whether this deck is being played.
        """
        if playing is None:
            self._playing = not self._active
        else:
            self._playing = playing

    def _handle_click(self, event):
        """Handles when the player clicks the deck."""
        # the index of the card in the deck
        slot = event.x // CARD_WIDTH

        if self.pick_card is not None and self._active:
            self.pick_card(slot)

    def get_card_view(self, card):
        """Determines the view class for a card.

        Parameters:
            card (Card): The card that requires a view.

        Returns:
            (CardView): The view for the given card.
        """
        return CARD_VIEWS.get(card.__class__, CardView)

    def draw_card(self, card, slot):
        """
        Draw a card in the given slot on the deck.

        Parameters:
            card (Card): The card to draw to the deck.
            slot (int): The position in the deck to draw the card.

        Returns:
            (CardView): The card view drawn at the slot for a given card.
        """
        left_side = slot * self.offset

        view = self.get_card_view(card)
        self.cards[slot] = view(self, left_side)

        return self.cards[slot]

    def draw(self, deck, show=True):
        """
        Draw the deck based of the data in a given deck instance.

        Parameter:
            deck (Deck): The deck to draw in this canvas.
            show (bool): Whether the cards should be displayed or not.
        """
        # resize the canvas to fit all the cards in the deck
        self.resize(deck.get_amount())

        # highlight border
        if self._playing:
            self.config(highlightbackground=self._active_border)
        else:
            self.config(highlightbackground=self._border_colour)

        for i, card in enumerate(deck.get_cards()):

            # retrieve the CardView class for this card
            view = self.cards.get(i, None)

            # draw the CardView if it doesn't exist already
            if view is None:
                view = self.draw_card(card, i)

            # if the type of card has changed, redraw the CardView
            if type(view) != self.get_card_view(card):
                view = self.draw_card(card, i)

            # update details in the CardView
            view.redraw(card if show else None)

    def resize(self, size):
        """
        Calculate the dimensions required to fit 'size' cards in this canvas
        and update the canvas size.

        Parameters:
            size (int): The amount of cards that should be displayed in this deck.
        """
        # ensure that the deck is at least one card wide
        if self.offset < CARD_WIDTH:
            width = (self.offset * size) + CARD_WIDTH
        else:
            width = (self.offset * size)

        height = CARD_HEIGHT

        # resize canvas, adjust for border
        self.config(width=width - 10, height=height - 10)


class UnoApp:
    """A graphical Uno application"""

    def __init__(self, master, game, board_colour="#F9B05A"):
        """Create a new Uno application based on a given UnoGame.

        Parameters:
            master (tk.Tk): The root window for the Uno application.
            game (UnoGame): The game to display in this application.
            board_colour (tk.Color): The background colour of the board.
        """
        self._master = master
        self.game = game
        self.board_colour = board_colour

        # define all the class variables
        self._board = self.decks = self._putdown_pile = self._pickup_pile \
            = self._special_pile = None

        self.render_decks()

        self.add_menu()

    def render_decks(self):
        # remove old frame, if it exists
        if self._board is not None:
            self._board.pack_forget()

        # create a board frame
        self._board = board = tk.Frame(self._master, padx=20, pady=20,
                                       bg=self.board_colour,
                                       borderwidth=2, relief="groove")
        board.pack(expand=True, fill=tk.BOTH)

        self.decks = decks = {}

        # split the board evenly
        split = len(self.game.players) // 2

        # draw the first decks of players
        for i, player in enumerate(self.game.players[:split]):
            decks[player] = self.draw_deck(player, show=False)
            self.draw_title(player)

        # draw the middle row of piles
        self._putdown_pile, self._pickup_pile, self._special_pile = self.draw_board()

        # draw the second decks of players
        for i, player in enumerate(self.game.players[split:]):
            decks[player] = self.draw_deck(player, show=False)
            self.draw_title(player)

    def update(self):
        """Redraw all the decks in the game."""
        # draw all player decks
        for player in self.game.players:
            playing = player == self.game.current_player()
            clickable = player.is_playable() and playing
            self.decks[player].toggle_active(active=clickable)
            self.decks[player].toggle_playing(playing=playing)
            self.decks[player].draw(player.get_deck(), show=clickable)

        # draw the pile decks
        self._putdown_pile.draw(self.game.putdown_pile)
        self._pickup_pile.draw(self.game.pickup_pile, show=False)
        self._special_pile.draw(self.game.special_pile)

    def new_game(self):
        """Start a new game"""
        # clone the old players
        players = []
        for player in self.game.players:
            players.append(player.__class__(player.get_name()))

        # generate a new deck
        pickup_pile = Deck(build_deck(FULL_DECK))
        pickup_pile.shuffle()

        # make players pickup cards
        for player in players:
            cards = pickup_pile.pick(7)
            player.get_deck().add_cards(cards)

        self.game = UnoGame(pickup_pile, players)
        self.render_decks()
        self.update()

    def add_menu(self):
        """Create a menu for the application"""
        menu = tk.Menu(self._master)

        # file menu with new game and exit
        file = tk.Menu(menu)
        file.add_command(label="New Game", command=self.new_game)
        file.add_command(label="Exit", command=self._master.destroy)

        # add file menu to menu
        menu.add_cascade(label="File", menu=file)
        self._master.config(menu=menu)

    def pick_card(self, player, slot):
        """Called when a given playable player selects a slot.

        Parameters:
            player (Player): The selecting player.
            slot (int): The card index they selected to play.
        """
        # get the selected card
        card = player.get_deck().get_cards()[slot]

        # pick the card if it matches
        if card.matches(self.game.putdown_pile.top()):
            card = player.get_deck().get_cards().pop(slot)
            self.game.select_card(player, card)

            # wait for next move
            self.step()

    def draw_card(self, _):
        """Pick up a card from the deck for the current player."""
        if not self.game.current_player().is_playable():
            return

        # select card from deck
        next_card = self.game.pickup_pile.pick()
        # add card to players deck
        self.game.current_player().get_deck().add_cards(next_card)

        # wait for next move
        self.step()

    def draw_board(self):
        """Draw the middle row of card piles to the board.

        Returns:
            tuple<DeckView, DeckView, DeckView>: The putdown, pickup and special
                                                 piles respectively.
        """
        board = tk.Frame(self._board, bg="#6D4C41")
        board.pack(side=tk.TOP, pady=20, fill=tk.X, expand=True)

        # left pickup card pile view
        pickup_pile = DeckView(board, offset=0, pick_card=self.draw_card)
        pickup_pile.toggle_active(active=True)
        pickup_pile.draw(self.game.putdown_pile, show=False)
        pickup_pile.pack(side=tk.LEFT, padx=50)

        # right putdown card pile view
        putdown_pile = DeckView(board, offset=2)
        putdown_pile.draw(self.game.putdown_pile)
        putdown_pile.pack(side=tk.RIGHT, padx=50)

        # middle right view for special cards
        special_pile = DeckView(board, offset=0)
        special_pile.draw(self.game.special_pile, show=False)
        special_pile.pack(side=tk.RIGHT)

        return putdown_pile, pickup_pile, special_pile

    def draw_deck(self, player, show=True):
        """Draw a players deck to the board

        Parameters:
            player (Player): The player whose deck should be drawn.
            show (bool): Whether or not to display the players deck.

        Returns:
            DeckView: The deck view for the player.
        """
        deck = DeckView(self._board,
                        pick_card=lambda card: self.pick_card(player, card))
        deck.pack(side=tk.TOP)
        deck.draw(player.get_deck(), show=show)
        return deck

    def draw_title(self, player):
        """Draw a deck label for a player to the board.

        Parameters:
            player (Player): The player to draw.
        """
        label = tk.Label(self._board, text=player.get_name(),
                         font=('Times', '24', 'bold italic'),
                         bg=self.board_colour)
        label.pack(side=tk.TOP)

    def step(self):
        """Perform actions to advance the game a turn."""
        # end the game if a player has won
        if self.game.is_over():
            messagebox.showinfo("Game Over",
                                f"{self.game.winner.get_name()} has won!")
            self._master.destroy()
            return

        # move to the next player
        player = self.game.next_player()
        self.update()

        # exit and wait for the player to make their move
        if player.is_playable():
            return

        self._master.after(AI_DELAY, self.take_turn)

    def take_turn(self):
        """Make an automated turn"""
        # make an automated move
        player = self.game.current_player()
        self.game.take_turn(player)
        self.update()

        self.step()

    def play(self):
        """Start the game running"""
        self.step()


def main():
    # create window for uno
    root = tk.Tk()
    root.title("Uno++")

    # build a list of players for the game
    players = [HumanPlayer("Ravi"), HumanPlayer(generate_name()),
               ComputerPlayer(generate_name())]

    # build a pickup pile
    pickup_pile = Deck(build_deck(FULL_DECK))
    pickup_pile.shuffle()

    # deal players cards from the pickup pile
    for player in players:
        cards = pickup_pile.pick(7)
        player.get_deck().add_cards(cards)

    # create and play the game
    game = UnoGame(pickup_pile, players)
    app = UnoApp(root, game)
    app.play()

    # update window dimensions
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()


if __name__ == "__main__":
    main()
