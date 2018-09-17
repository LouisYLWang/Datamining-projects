#####################################################
#######        COMPUTATIONAL BIOLOGY         ########
#######             HOMEWORK 1               ########
#####################################################
#                                                   #
# Implement the pairwise alignment algorithms       #
# Needleman-Wunsch and Smith-Waterman.              #
#                                                   #
#####################################################
#####################################################

# In all functions the following parameters are the same:
# seqA: the first sequence to align
# seqB: the second sequence to align
# score_gap: score for a gap
# score_match: score for a character match
# score_mismatch: score for a character mismatch
# local: True if alignment is local, False otherwise


rm(list=ls())

init_score_matrix = function(nrow, ncol, local, score_gap) {
  # Initialize the score matrix with zeros.
  score_matrix<-matrix(0,nrow,ncol)
  # If the alignment is global, the leftmost column and the top row will have incremental gap scores,
  # i.e. if the gap score is -2 and the number of columns is 4, the top row will be [0, -2, -4, -6].
  if(local==FALSE){
    score_matrix[,1]<-seq(from=0,to=score_gap*(nrow-1),by=score_gap)
    score_matrix[1,]<-seq(from=0,to=score_gap*(ncol-1),by=score_gap)
  } 
  # nrow: number of rows in the matrix
  # ncol: number of columns in the matrix
  # Return the initialized empty score matrix
  # score_matrix: nrow by ncol matrix
  return(score_matrix)
}


init_path_matrix = function(nrow, ncol) {
  # Initialize the path matrix with empty values, except the top row and the leftmost column.
  # The top row has "left" on all positions except 1st.
  # The leftmost column has "up" on all positions except 1st.
  # nrow: number of rows in the matrix
  # ncol: number of columns in the matrix
  path_matrix<-matrix(NA,nrow,ncol)
  path_matrix[1,2:ncol]<-'left'
  path_matrix[2:nrow,1]<-'up'
  # Return the initialized empty path matrix
  # path_matrix: nrow by ncol matrix
  return(path_matrix)
}

get_best_score_and_path = function(row, col, seqA, seqB, score_matrix, score_gap, score_match, score_mismatch, local){
  # Compute the score and the best path for a particular position in the score matrix
  # row: row-wise position in the matrix
  # col: column-wise position in the matrix
  # score_matrix: the score_matrix that is being filled out
  a<-0
  b<-score_matrix[row-1,col-1]+ifelse(substr(seqA,col-1,col-1)==substr(seqB,row-1,row-1),score_match,score_mismatch)
  c<-score_matrix[row-1,col]+score_gap
  d<-score_matrix[row,col-1]+score_gap
  score<-max(a,b,c,d)
  if(local==FALSE){
    score<-max(b,c,d)
  }
  if(score==b){
    path<-"diag"
  }
  else if(score==c){
    path<-"up"
  }
  else{
    path<-"left"
  }
  # Return the best score for the particular position in the score matrix
  # In the case that there are several equally good paths available, return any one of them.
  # score: best score at this position
  # path: path corresponding to the best score, one of ["diag", "up", "left"]
  return(list("score"=score, "path"=path))
}

fill_matrices = function(seqA, seqB, score_gap, score_match, score_mismatch, local, score_matrix, path_matrix) {
  # Compute the full score and path matrices
  # score_matrix: initial matrix of the scores
  # path_matrix: initial matrix of paths
  for(i in 2:(nchar(seqB)+1)){
    for(j in 2:(nchar(seqA)+1)){
      score_matrix[i,j]<-unlist(get_best_score_and_path(i,j,seqA,seqB,score_matrix,score_gap,score_match,score_mismatch,local)[[1]])
      path_matrix[i,j]<-unlist(get_best_score_and_path(i,j,seqA,seqB,score_matrix,score_gap,score_match,score_mismatch,local)[[2]])   
    }
  }
  # Return the full score and path matrices
  # score_matrix: filled up matrix of the scores
  # path_matrix: filled up matrix of paths
  return(list("score_matrix"=score_matrix, "path_matrix"=path_matrix))
}


get_best_move = function(seqA, seqB, path, row, col) {
  # Compute the aligned characters at the given position in the score matrix and return the new position,
  # i.e. if the path is diagonal both the characters in seqA and seqB should be added,
  # if the path is up or left, there is a gap in one of the sequences.
  # path: best path pre-computed for the given position
  # row: row-wise position in the matrix
  # col: column-wise position in the matrix
  if(path=='diag'){
    char1<-substr(seqA,col-1,col-1)
    char2<-substr(seqB,row-1,row-1)
    newrow<-row-1
    newcol<-col-1
  }
  else if(path=='up'){
    char1<-'-'
    char2<-substr(seqB,row-1,row-1)
    newrow<-row-1
    newcol<-col
  }
  else if(path=='left'){
    char1<-substr(seqA,col-1,col-1)
    char2<-'-'
    newrow<-row
    newcol<-col-1
  }
  # Return the new row and column and the aligned characters
  # newrow: row if gap in seqA, row - 1 if a match
  # newcol: col if gap in seqB, col - 1 if a match
  # char1: '-' if gap in seqA, appropriate character if a match
  # char2: '-' if gap in seqB, appropriate character if a match
  return(list("newrow"=newrow, "newcol"=newcol, "char1"=char1, "char2"=char2))
}


get_best_alignment = function(seqA, seqB, score_matrix, path_matrix, local) {
  # Return the best alignment from the pre-computed score matrix
  # score_matrix: filled up matrix of the scores
  # path_matrix: filled up matrix of paths
  alignment<-c()
  sA<-''
  sB<-''
  if(local==TRUE){
    score<-max(score_matrix)
    position<-which(score_matrix==score_matrix[which.max(score_matrix)],arr.ind=TRUE)
    row<-position[1,'row']
    col<-position[1,'col']
    while(score_matrix[row,col]>0){
      path<-path_matrix[row,col]
      position<-get_best_move(seqA,seqB,path,row,col)[1:2]
      sA<-paste(get_best_move(seqA, seqB, path, row, col)[[3]],sA)
      sB<-paste(get_best_move(seqA, seqB, path, row, col)[[4]],sB)
      row<-unlist(position[1])
      col<-unlist(position[2])
    }
  }
  else if(local==FALSE){
    score<-score_matrix[nchar(seqB)+1,nchar(seqA)+1]
    row<-nchar(seqB)+1
    col<-nchar(seqA)+1
    while(row*col!=1){
      path<-path_matrix[row,col]
      position<-get_best_move(seqA,seqB,path,row,col)[1:2]
      sA<-paste(get_best_move(seqA, seqB, path, row, col)[[3]],sA)
      sB<-paste(get_best_move(seqA, seqB, path, row, col)[[4]],sB)
      row<-unlist(position[1])
      col<-unlist(position[2])
    }
  }
  
  #sA<-paste(get_best_move(seqA, seqB, path_matrix[2,2], 2, 2)[[3]],sA)
  #sB <- paste(get_best_move(seqA, seqB, path_matrix[2,2], 2, 2)[[4]],sB)
  alignment<-c(sA,sB)
  # Return the best score and alignment (or one thereof if there are multiple with equal score)
  # score: score of the best alignment
  # alignment: the actual alignment in the form of a vector of two strings
  return(list("score"=score, "alignment"=alignment))
}


align = function(seqA, seqB, score_gap, score_match, score_mismatch, local) {
  # Align the two sequences given the scoring scheme
  # For testing purposes, use seqA for the columns and seqB for the rows of the matrices
  
  # Initialize score and path matrices
  score_matrix<-init_score_matrix(nchar(seqA)+1, nchar(seqB)+1, local, score_gap)
  path_matrix<-init_path_matrix(nchar(seqA)+1, nchar(seqB)+1)
  # Fill in the matrices with scores and paths using dynamic programming
  matrices<-fill_matrices(seqA, seqB, score_gap, score_match, score_mismatch, local, score_matrix, path_matrix)
  
  # Get the best score and alignment (or one thereof if there are multiple with equal score)
  result<- get_best_alignment(seqA, seqB, matrices[[1]], matrices[[2]], local)
  
  # Return the best score and alignment (or one thereof if there are multiple with equal score)
  # Returns the same value types as get_best_alignment
  return(result)
}


align('AGAC','AATC',-2,3,-1,T)

score_gap = -2
score_match = +3
score_mismatch = -1
align("TCACACGT", "AGCACACT", score_gap, score_match, score_mismatch, T)#"CACACGT""CACAC-T"
align("TCTGAGTA", "ACGAGCTA", score_gap, score_match, score_mismatch, F)#"TCTGAGTA", "ACGAGCTA"
align("TCTGAGTA", "ACGTGCTA", score_gap, score_match, score_mismatch, T)#"C-TGAGTA","C-TGAGTA","CTGAG-TA"  
align("TGAGAGTA", "ACGAGAGA", score_gap, score_match, score_mismatch, F)
align("TCTGAGTA", "ACGAGCTA", score_gap, score_match, score_mismatch, F)#"TCTGAG-TA", "AC-GAGCTA"
align("TGAGAGTA", "ACGAGAGA", score_gap, score_match, score_mismatch, F)#("-TGAGAGTA","T-GAGAGTA")("ACGAGAG-A")
