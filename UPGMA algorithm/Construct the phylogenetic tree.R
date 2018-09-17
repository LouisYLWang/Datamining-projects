#########################################################
#######        COMPUTATIONAL BIOLOGY         ############
#######             HOMEWORK 3               ############
#########################################################
#                                                       #
# Reconstruct the phylogenetic tree of given sequences  #
# using UPGMA with various distances measures.          #
#                                                       #
#########################################################
#########################################################

#########################################################
######    Code below this should not be changed   #######
#########################################################

library(ape)
rm(list=ls())
transform_to_phylo = function(sequences, named_edges, edge_lengths, node_description) {
    # Produce a tree of the phylo class from the matrix of edges, vector of lengths and
    # the dataframe  containing node descriptions.
    #    sequences: a list of the original sequences;
    #    named_edges: an Mx2 matrix of pairs of nodes connected by an edge,
    #                 where the M rows are the different edges and the 2 columns
    #                 are the parent node and the child node of an edge.
    #    edge_lengths: a vector of length M of the corresponding edge lengths.
    #    node_description: a data frame of the node descriptions as defined in
    #                      initialize_node_description and extended by the upgma code.
    
    edges = named_edges
    for (name in rownames(node_description)) {
        index = which(rownames(node_description) == name)
        edges[which(edges == name)] = as.numeric(index)
    }
    edges = matrix(as.numeric(edges), ncol = 2)
    
    edges[which(edges > length(sequences))] = - edges[which(edges > length(sequences))]
    root = setdiff(edges[,1], edges[,2])
    edges[which(edges==root)] = length(sequences) + 1
    
    k = length(sequences) + 2
    for(x in unique(edges[which(edges < 0)])) {
        edges[which(edges==x)] = k
        k = k + 1
    }
    
    tree = list()
    class(tree) = "phylo"
    tree$edge = edges
    tree$edge.length = edge_lengths
    tree$Nnode = as.integer(length(sequences) - 1)
    tree$tip.label = names(sequences)
    
    # Return the tree in the form of the phylo class from ape
    return(tree)
}

plot_tree = function(tree) {
    # Plot the phylogenetic tree with node labels and edge lengths.
    #    tree: an object of class phylo from the ape package

    plot(tree)
    edgelabels(format(tree$edge.length, digits = 2))
}

initialize_node_description = function(sequences) {
    # Initialize the structure that will hold node descriptions.
    # The created structure is a data frame where the rows are node names, and the columns are
    # node_height -- distance from the node to any tip in the ultrametric tree, and
    # node_size -- number of tips that this node is ancestral to.
    #    sequences: a list of the original sequences;

    N = length(sequences)
    node_names = names(sequences)
    node_sizes = rep(1, times = N)
    node_heights = rep(0, times = N)
    node_description = data.frame(node_sizes, node_heights)
    rownames(node_description) = node_names

    # Return a data frame that contains information on currently existing tip nodes.
    # node_description: a dataframe containing information on the currently existing nodes.
    #                   The row names are the names of the currently existing tips, i.e.
    #                   are the same as the names in the sequence list, node_height is
    #                   0 and node_size is 1 as the all the currently existing nodes are tips.
    return(node_description)
}



add_new_node = function(node_description, merging_nodes) {
    # Add new merged node to the node description data frame.
    # The new node is a combination of the nodes supplied in the merging_nodes,
    # e.g. if one needs to merge nodes "bird" and "fish", the new node in the
    # dataframe will be called "bird.fish".
    #    node_description: the dataframe created by initialize_node_description, containing
    #                      current node sizes and node heights
    #    merging_nodes: a vector of two names of the nodes being merged

    new_node_name = paste(merging_nodes, collapse = ".")
    new_node_row = data.frame(node_sizes = 0, node_heights = 0)
    rownames(new_node_row) = new_node_name
    new_node_description = rbind(node_description, new_node_row)
    
    # Return the node_description dataframe with a row for the new node added, and
    # the new node name.
    #    node_description: the dataframe where the rows are labelled by current nodes and columns
    #                      contain the node heights and sizes.
    #    new_node_name: the name of the newly added node, created from names in merging_nodes.
    return(list(node_description = new_node_description, new_node_name = new_node_name))
}

#########################################################
######    Code above this should not be changed   #######
#########################################################


get_hamming_distance = function(sequence1, sequence2) {
  # Compute the Hamming distance between two sequences.
  #    sequence1: first sequence 
  #    sequence2: second sequence
  distance<-0
  for(i in 1:nchar(sequence1)){
    if(substr(sequence1,i,i)!=substr(sequence2,i,i)){
      distance<-distance+1
    }
  }
  # Return the numerical value of the distance
  return(distance)
}

get_JC69_distance = function(sequence1, sequence2) {
  # Compute the JC69 distance between two sequences.
  #    sequence1: first sequence
  #    sequence2: second sequence
  H<-0
  for(i in 1:nchar(sequence1)){
    if(substr(sequence1,i,i)!=substr(sequence2,i,i)){
      H<-H+1
    }
  }
  L<-nchar(sequence1)
  distance<-(-3/4)*log(1-3*H/(4*L))
  # Return the numerical value of the distance
  return(distance)
}

get_K80_distance = function(sequence1, sequence2) {
  # Compute the K80 distance between two sequences.
  #    sequence1: first sequence
  #    sequence2: second sequence
  sequence1<-gsub('A',1,sequence1)
  sequence1<-gsub('T',3,sequence1)
  sequence1<-gsub('G',6,sequence1)
  sequence1<-gsub('C',7,sequence1)
  sequence2<-gsub('A',1,sequence2)
  sequence2<-gsub('T',3,sequence2)
  sequence2<-gsub('G',6,sequence2)
  sequence2<-gsub('C',7,sequence2)
  transition<-0
  transversion<-0
  sum<-c()
  for(i in 1:nchar(sequence1)){
    sum[i]<-as.numeric(substr(sequence1,i,i))+as.numeric(substr(sequence2,i,i))
    if(sum[i]==10|sum[i]==7){
      transition<-transition+1
    }
    if(sum[i]==8|sum[i]==4|sum[i]==13|sum[i]==9){
      transversion<-transversion+1
    }
  }
  S<-transition/nchar(sequence1)
  V<-transversion/nchar(sequence1)
  distance<-(-0.5)*log(1-2*S-V)-0.25*log(1-2*V)
  # Return the numerical value of the distance
  return(distance)
}

compute_initial_distance_matrix = function(sequences, distance_measure) {
  # Compute the initial distance matrix using one of the distance measures.
  # The matrix is of dimension NxN, where N is the number of sequences.
  # The matrix columns and rows should be labelled with tip names, each row and column
  # corresponding to the appropriate sequence.
  # The matrix can be filled completely (i.e symmetric matrix) or only the upper half (as shown in the lecture).
  # The diagonal elements of the matrix should be Inf.
  #    sequences: the sequences in the format of a list of species names and the associated genetic sequences
  #    distance_measure: a string indicating whether the 'hamming', 'JC69' or 'K80' distance measure should be used
  
  N = length(sequences)
  distance_matrix = matrix(nrow = N, ncol = N)
  rownames(distance_matrix) = names(sequences)
  colnames(distance_matrix) = names(sequences)
  for (i in names(sequences)){
    for (j in names(sequences)){
      distance_matrix[i,j]<-switch(distance_measure,
                                   "hamming"= get_hamming_distance(sequences[i],sequences[j]),
                                   "JC69"= get_JC69_distance(sequences[i],sequences[j]),
                                   "K80"= get_K80_distance(sequences[i],sequences[j]))
    }
  }
  diag(distance_matrix) = Inf

  # Return the NxN matrix of inter-sequence distances with Inf on the diagonal
  return(distance_matrix)
}


get_merge_node_distance = function(merging_nodes, existing_node, node_description, distance_matrix) {
  # Compute the new distance between the newly created merge node and the old node in the tree (possibly also a node)
  #    merging_nodes: a vector of two node names that need to be merged in this step;
  #    existing_node: one of the previously existing nodes, not included in the new node;
  #    node_description: a dataframe containing information on the currently existing nodes;
  #    distance_matrix: the matrix of current distances between nodes.
  
  #
  new_distance <- sum(node_description[merging_nodes[1],1]*distance_matrix[merging_nodes[1],existing_node],
                      node_description[merging_nodes[2],1]*distance_matrix[merging_nodes[2],existing_node])/sum(
                      node_description[merging_nodes[1],1],node_description[merging_nodes[2],1])
                      
  # Returns the new distance between the newly created node and the existing node
  return(new_distance)
}

     
update_distance_matrix = function(distance_matrix, merging_nodes, new_node_name, node_description) {
  # Update the distance matrix given that two nodes are being merged.
  #    distance_matrix: the current distance matrix that needs to be updated
  #    merging_nodes: a vector of two node names that need to be merged in this step
  #    new_node_name: the name with which the merged node should be labelled
  #    node_description: a dataframe containing information on the currently existing nodes;
  # The resulting matrix should be one column and one row smaller, i.e. if the given distance matrix was
  # MxM, then the updated matrix will be M-1xM-1, where the 2 rows and cols represent the separate nodes
  # undergoing merge are taken out and a new row and col added that represents the new node
  
  distance_matrix<-rbind(distance_matrix,0)
  distance_matrix<-cbind(distance_matrix,0)
  rownames(distance_matrix)[nrow(distance_matrix)]<-new_node_name
  colnames(distance_matrix)[ncol(distance_matrix)]<-new_node_name

  for (i in setdiff(colnames(distance_matrix),merging_nodes)){
    merge_node_distance <-get_merge_node_distance(merging_nodes,i,node_description,distance_matrix)
    distance_matrix[i,new_node_name]<-merge_node_distance
    distance_matrix[new_node_name,i]<-merge_node_distance
  } 
  
  del_index <- c(-which(rownames(distance_matrix)==merging_nodes[1]),
                 -which(rownames(distance_matrix)==merging_nodes[2]))
  diag(distance_matrix) = Inf
  updated_distance_matrix<-distance_matrix[del_index,del_index]
  
  # Returns the updated matrix of cluster distances
  return(updated_distance_matrix)
}



upgma_one_step = function(distance_matrix, edges, edge_lengths, node_description) {
  # Performs one step of the upgma algorithm, i.e. the nodes with the smallest distance are merged, the node height of the new node is calculated and the distance matrix is newly calculated. Values that are expected to be returned are listed below.
  #    sequences: the list of sequences to get the tree from.
  #    initial_distance_matrix: the initial distance matrix.
  # The matrix is NxN entries, where N is the number of sequences.
  # The matrix columns and rows are labelled with tip numbers from 1 to N, each row and column corresponding
  # to the appropriate sequence -- e.g. row i corresponds to sequences[i].
  # The diagonal elements of the matrix are Inf.
  
  merging_nodes <- rownames(which(distance_matrix==min(distance_matrix),arr.ind=TRUE))
  new_node_name <- add_new_node(node_description, merging_nodes)$new_node_name
  node_description <- add_new_node(node_description, merging_nodes)$node_description
  node_description[new_node_name,]$ node_sizes <- sum(node_description[merging_nodes,]$node_sizes)
  node_description[new_node_name,]$ node_heights <- distance_matrix[merging_nodes[2],merging_nodes[1]]/2
  
  edges<-rbind(edges,cbind(new_node_name,merging_nodes))
  
  new_height<-distance_matrix[merging_nodes[2],merging_nodes[1]]/2
  edge_lengths<-c(edge_lengths,new_height-node_description[merging_nodes[1],"node_heights"])
  edge_lengths<-c(edge_lengths,new_height-node_description[merging_nodes[2],"node_heights"])
  
  #edge_lengths <- c(edge_lengths,  rep(distance_matrix[merging_nodes[2],merging_nodes[1]]/2,2))
  distance_matrix <- update_distance_matrix(distance_matrix, merging_nodes, new_node_name, node_description)

  # Return the updated edge description matrix, edge length vector and node_description data frame
  #    edges: an Mx2 matrix of pairs of nodes connected by an edge, where the M rows are the different edges
  #           and the 2 columns are the parent node and the child node of an edge.
  #    edge_lengths: a vector of length M of the corresponding edge lengths.
  #    node_description: data frame containing sizes and heights of all nodes (to be updated with the help of add_new_node())
  return(list(distance_matrix = distance_matrix, edges = edges, edge_lengths = edge_lengths, node_description = node_description))
}

build_upgma_tree = function(sequences, distance_measure) {
  # Build the tree from given sequences.
  #    sequences: the sequences in the format of a list of species names and the associated genetic sequences
  #    distance_measure: a string indicating whether the 'hamming', 'JC69' or 'K80' distance measure should be used
  N = length(sequences)
  node_description = initialize_node_description(sequences)
  edges = matrix(nrow = 0, ncol = 2)
  edge_lengths = vector(mode = "numeric", length = 0)
  distance_matrix<-compute_initial_distance_matrix(sequences,distance_measure)
  while(length(distance_matrix)>1){
    result<-upgma_one_step(distance_matrix, edges, edge_lengths, node_description) 
    distance_matrix = result$distance_matrix
    edges = result$edges
    edge_lengths = result$edge_lengths
    node_description = result$node_description
  }
  #rec <-function(distance_matrix, edges, edge_lengths, node_description){
  #  if (length(distance_matrix)>1){
  #    return (rec(distance_matrix, edges, edge_lengths, node_description))
  #  }
  #  else{
  #    return(edges, edge_lengths, node_description)
  #  }
  #}
  #Return the UPGMA tree of sequences
  tree = transform_to_phylo(sequences, edges, edge_lengths, node_description) 
  return(tree)
}

test_tree_building = function() {
  sequences = list(orangutan = "CTGCTACTGAAACCAGACTA",
                   gorilla = "CTGCTGTTTAGAAAAAACTA",
                   chimp = "CTGCTGTTTAGTAAGAACCA",
                   human = "CTGCTGTTTAGTAAGAACTA")
  #distance_measure = 'hamming'
  #distance_measure = 'JC69'
  distance_measure = 'K80'
  
  tree = build_upgma_tree(sequences, distance_measure)
  plot_tree(tree)
}



test_tree_building()




