# Guts 2023 Hackathon
## JP Morgan challenge - Escape/Puzzle Room
### Ideas

UI
- screen split into three sections (columns)
- actions on left hand side - always present
- ui elements in the middle
    - inventory
    - rooms
- log of actions taken on the right

Puzzles
- start off easy, get progressively harder
- room 1
    - start off in room with a bookshelf, tv, dvd shelf
    - look at bookshelf
        - your attention is drawn to the poem "Paradise Lost"
    - look at dvd shelf
        - you feel nostalgia for the movie "Return of the King"
    - look at the tv
        - the screen flickers on and you read the words "Where do the eagles not dare in 2003?"
    - pick up tv remote
        - can use it on the tv
        - player should enter "Mordor" to answer the question
        - a hidden passage in the room opens
    - player can go to the next room


- room 2
    - next room is a hallway with five doors
    - there is a key on the floor when you enter
    - look at the key
        - there is a note attached to the key saying "fib 3"
            - the third fibonacci number is 2
            - the key opens the second door

Objects

- Room
    - list of items in the room
    - list of static interactive things in the room
    - list of adjoining rooms
        - keep track of which rooms are locked

- Static Interactive
    - description
    - items that it can interact with

- Item - inherits from Static Interactive
    - description
    - action item can take
    - objects it can be used on (?)

- Player
    - items in their inventory
    - which room they are in
    - move method to change rooms

- Map
    - 2D array of rooms