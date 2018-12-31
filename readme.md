<html>
    <h1>Three Musketeers game</h1>
    <p>The repository contains an implimentation of the base program and extended program with strategies.</p>
    <h1>Extended Program with Strategies</h1>
    <p>In terms of user interaction, the following changes have been made relative to the base implementation:</p>
    <ul>
      <li> Change to user input to select game difficulty, three difficulties can be specified:</li>
      <li> Easy: computer makes legal move at random, as base implementation.</li>
      <li> Medium: computer makes logical move at random (Cardinal Richelieu's men will extend game by moving orthogonally to the Musketeers, the Musketeers will avoid moving in to a common row/column if other options exist).</li>
      <li>Hard: computer makes tactical move (Cardinal Richelieu's men will follow tactic to preferentially draw the Musketeers is a common direction, the Musketeers will move to create the greatest area between there locations).</li>
      <li>When the computer plays as Cardinal Richelieu's men on hard difficulty, a random tactic is generated to specify a direction in which the Musketeers will be drawn –  as the tactic is created as a global variable, it is encrypted to avoid is being displayed to player if played in IDE.</li>
    </ul>
    <h1>Evaluating Tactics</h1>
    <p>A number of tactics were theorised and implemented in addition to those implemented within the extended program for both Cardinal Richelieu's men and the Musketeers. In order to assess the effectiveness of each tactic, code was written to provide summary statistics for a large number of simulated games (function play_sim).</p>
    <p>Given the three musketeers is an asymmetrical game, where both sides are making random moves (easy difficulty), Cardinal Richelieu's men will only win approximately 16% of the time. It has been shown that when an optimal tactic for the Musketeers is played, they will always win (Elabridi, 2017).</p>
    <p>The following statistics demonstrate the effectiveness of each tactic, when 1000 games were simulated against an opponent of medium difficulty:</p>
    <table>
  <tr>
    <th>Musketeer Difficulty</th>
    <th>Cardinal Richelieu win percent</th> 
    <th>Cardinal Richelieu difficulty</th>
    <th>Cardinal Richelieu win percent</th> 
  </tr>
  <tr>
    <th>Easy</th>
    <th>14.6</th> 
    <th>Easy</th>
    <th>2.6</th> 
  </tr>
  <tr>
    <th>Medium</th>
    <th>2.7</th> 
    <th>Medium</th>
    <th>2.9</th> 
  </tr>
    <tr>
    <th>Hard</th>
    <th>0.1</th> 
    <th>Hard</th>
    <th>5.7</th> 
  </tr>
</table>
    <p>It can be seen the computer strategy chosen can vary the difficulty of the game in a relative sense, but cannot compensate for the underlying asymmetry in the game.</p>
    <h1>References</h1>
    <p>Elabridi, A., 2017, Weakly solving the three musketeers game using artificial intelligence and game theory. Capstone Project. Al Akhawayn University.</p>
 </html>
