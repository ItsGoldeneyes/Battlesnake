function decideMove(gameState: GameState, myself: Battlesnake, lookahead?: number): MoveWithEval { // MoveWithEval is a direction & a numeric score
	let evalThisState: number = evaluate(gameState, myself)
	let availableMoves: Direction[] = getAvailableMoves(gameState, myself)
	let bestMove: MoveWithEval = undefined
	for (move of availableMoves) {
		let newGameState: GameState = cloneGameState(gameState)
		let newSelf: Battlesnake = newGameState.board.snakes.find(snake => snake.id === myself.id)
		let otherSnakes: Battlesnake[] = newGameState.board.snakes.filter(snake => snake.id !== myself.id)
		moveSnake(newGameState, newSelf, move)
		if (myself.id === gameState.you.id) { // if decideMove is deciding for myself, let each other snake also think about where to go
			for (snake of otherSnakes) {
				let snakeMove: MoveWithEval = decideMove(gameState, snake, 0)
				moveSnake(newGameState, snake, snakeMove.direction)
			}
		} else { // if decideMove is deciding for other snakes, do not let each other snake think about where to go, else infinite loop
			for (snake of otherSnakes) {
				fakeMoveSnake(newGameState, snake) // just remove tail & duplicate head
			}
		}
		updateGameStateAfterMove(newGameState) // does things like updating turn, lowering healths, removing eaten food, removing dead snakes, etc.
		
		let evalState: MoveWithEval
		if (lookahead > 0) {
			evalState = decideMove(newGameState, newSelf, lookahead - 1)
		} else {
			evalState = new MoveWithEval(move, evaluate(newGameState, newSelf))
		}
		
		if (bestMove) {
			if (evalState.score > bestMove.score) {
				bestMove.direction = move
				bestMove.score = evalState.score
			}
		} else {
			bestMove.direction = move
			bestMove.score = evalState.score
		}
	}
	
	bestMove.score = bestMove.score + evalThisState // this is the cumulative part, where the current state score is added with the next state score
	
	return bestMove
}
