library(igraph)
library(SparseM)

# setup edgelist + grid to look at
sample_grid = function(N_x, N_y, xlim = c(-1,1), ylim = c(-1,1)) {

  
  # bounding box 
  min_x <- xlim[1]
  max_x <- xlim[2]
  min_y <- ylim[1]
  max_y <- ylim[2]

  
  x_locs <- seq(0, N_x)
  y_locs <- seq(0, N_y)
  
  N_grid <- N_x * N_y
  
  x <- rep(0, length(N_grid))
  y <- rep(0, length(N_grid))
  
  for(i in 1:N_x){
    for(j in 1:N_y) {
      x[N_y * (i-1) + j] <- x_locs[i]
      y[N_y * (i-1) + j] <- y_locs[j]
    }
  }
  
  locations <- cbind(x,y)
  
  return(locations)
}

N_x <- 10
N_y <- 10

# node locations
Vert <- sample_grid(N_x,N_y)

# edges...

# horizontally...
fromH <- c()
for(i in 1:(N_x-1)){
  fromH <- c(fromH, seq(0,(N_y*N_x-N_x), length.out = (N_y)) + i)
}
toH <- fromH + 1

# vertically...
fromV <- 1:(N_x*N_y-N_x)
toV <- fromV + N_x

# --------------------------------------------------------------------------------------------
# crux

Edges <- data.frame(from = c(fromH, fromV), to = c(toH, toV)) # , weights = rep(1,(2*N_x*N_y - (N_x+N_y))))     

# change the weights up
set.seed(1)
weight <- rlnorm(n = nrow(Edges), meanlog = 0, sdlog = 1)
Edges$weight <- weight

the_graph <- graph_from_data_frame(Edges, directed = FALSE)
lo <- layout.norm(as.matrix(Vert))
plot(the_graph, layout = lo, directed = FALSE, edge.arrow.size=0)


# solving
L <- laplacian_matrix(the_graph, weights = weight)

# boundary conditions on 68, 12: 
# draw 1 amp @ 12
# inject 1 amp @ 68

q <- matrix(rep(0, nrow(Vert)), ncol = 1)
q[68,] <- +1
q[12,] <- -1

# solve
p <- solve(L,q)


R <- p[68,] - p[12,]


# investigating why the weights aren't working! (wrong first attempt)
# neighbours <- c(78,58,67,69)  # neighbours of node 68
# neighbours_weights <- weight[neighbours]
# neighbours_potential_diffs <- p[68,] - p[neighbours,]
# neighbours_currents <- neighbours_potential_diffs * neighbours_weights

neighbours <- which(Edges$from == 68 | Edges$to == 68)
potential_diffs <- p[Edges$from,] - p[Edges$to,]
currents <- potential_diffs * Edges$weight
what <- cbind(Edges,p[Edges$from,], p[Edges$to,], currents)
what[neighbours,]



# exact solution for effective resistance between 68 and 12 with 10x10 and all 1ohm
exact <- 455859137025721/283319837425200