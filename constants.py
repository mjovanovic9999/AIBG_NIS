INFANTRY=0
GUNNER=1
MORTAR=2
COMMANDO=3

ALPHA_START=-10000000
BETA_START=10000000

MINMAX_DEPTH = 3
CUTOFF=2


#DA L (0,0)???????????
INFANTRY_PLACE_MATRIX=[
                       (-3,0),
               (-2,-1),(-2,0),(-2,1),
       (-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),
  (0,-3),(0,-2),(0,-1),        (0,1),(0,2),(0,3),
          (1,-2),(1,-1),(1,0),(1,1),(1,2),
                 (2,-1),(2,0),(2,1),
                        (3,0),
]

GUNNER_PLACE_MATRIX=[
              (-1,0),
         (0,-1),   (0,1),
               (1,0),
]

MORTAR_PLACE_MATRIX=[ 
               (-2,0),
       (-1,-1),(-1,0),(-1,1),
    (0,-2),(0,-1),   (0,1),(0,2),
         (1,-1),(1,0),(1,1),
                (2,0),
                        
]

COMMANDO_PLACE_MATRIX=[
                       (-3,0),
               (-2,-1),(-2,0),(-2,1),
       (-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),
  (0,-3),(0,-2),(0,-1),        (0,1),(0,2),(0,3),
          (1,-2),(1,-1),(1,0),(1,1),(1,2),
                 (2,-1),(2,0),(2,1),
                        (3,0),
]
######attack
INFANTRY_ATTACK_MATRIX=[
                (-2,0),
                (-1,0),
    (0,-2),(0,-1),   (0,1),(0,2),
                 (1,0),
                 (2,0),
]

GUNNER_ATTACK_MATRIX=[ 
                       (-3,0),
               (-2,-1),(-2,0),(-2,1),
       (-1,-2),(-1,-1),       (-1,1),(-1,2),
    (0,-3),(0,-2),                     (0,2),(0,3),
          (1,-2),(1,-1),       (1,1),(1,2),
                 (2,-1),(2,0),(2,1),
                        (3,0),
]

MORTAR_ATTACK_MATRIX=[
                         (-4,0),
     (-3,-3),            (-3,0),              (-3,3), 
            (-2,-2),     (-2,0),        (-2,2),
                                
(0,-4),(0,-3),(0,-2),                     (0,2),(0,3),(0,4),
                                        
             (2,-2),      (2,0),         (2,2),
      (3,-3),             (3,0),               (3,3),
                          (4,0),
]

COMMANDO_ATTACK_MATRIX=[#special
                       (-3,0),
               (-2,-1),(-2,0),(-2,1),
       (-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),
  (0,-3),(0,-2),(0,-1),        (0,1),(0,2),(0,3),
          (1,-2),(1,-1),(1,0),(1,1),(1,2),
                 (2,-1),(2,0),(2,1),
                        (3,0),
]