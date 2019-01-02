<html>
    <h1>Three Musketeers game</h1>
    <p>The repository contains an implimentation of the base program and extended program with strategies.</p>
    <h1>Extended Program with Strategies</h1>
    <p>In terms of user interaction, the following changes have been made relative to the base implementation:</p>
    <ul>
      <li> Change to user input to select game difficulty, three difficulties can be specified:</li>
      <ul>
          <li> Easy: computer makes legal move at random, as base implementation.</li>
          <li> Medium: computer makes logical move at random (Cardinal Richelieu's men will extend game by creating orthogonal moves for the Musketeers in a common direction if possible, the Musketeers will avoid moving in to a common row/column if possible).</li>
          <li>Hard: computer makes tactical move (Cardinal Richelieu's men will block the Musketeers from progressing in a common direction if possible, the Musketeers move to create the greatest area between board locations).</li>
      </ul>
      <li>When the computer plays as Cardinal Richelieu's men on hard difficulty, a random tactic is generated to specify a direction in which the Musketeers are drawn –  as the tactic is created as a global variable, it is weakly encrypted to avoid it being displayed to player through IDE.</li>
    </ul>
    <h1>Evaluating Tactics</h1>
    <p>A number of tactics were theorised and implemented in addition to those implemented within the extended program for both Cardinal Richelieu's men and the Musketeers. In order to assess the effectiveness of each tactic, code was written to provide summary statistics for a large number of simulated games (function play_sim).</p>
    <p>Given the Three Musketeers is an asymmetrical game - where both sides are making random moves (easy difficulty), Cardinal Richelieu's men will only win approximately 16% of the time. It has been shown that when an optimal tactic for the Musketeers is played, they will always win (Elabridi, 2017).</p>
    <p>The following statistics demonstrate the effectiveness of each tactic, when 2000 games were simulated against an opponent of medium difficulty:</p>
    <table>
  <tbody><tr>
    <th>Musketeer Difficulty</th>
    <th>Cardinal Richelieu win percent</th> 
    <th>Cardinal Richelieu difficulty</th>
    <th>Cardinal Richelieu win percent</th> 
  </tr>
  <tr>
    <th>Easy</th>
    <th>17.2</th> 
    <th>Easy</th>
    <th>9.3</th> 
  </tr>
  <tr>
    <th>Medium</th>
    <th>13.4</th> 
    <th>Medium</th>
    <th>13.4</th> 
  </tr>
    <tr>
    <th>Hard</th>
    <th>0.1</th> 
    <th>Hard</th>
    <th>16.0</th> 
  </tr>
</tbody></table>
    <p>It can be seen the computer strategy chosen can vary the difficulty of the game in a relative sense, but cannot compensate for the underlying asymmetry in the game.</p>
    <h1>References</h1>
    <p>Elabridi, A., 2017, Weakly solving the three musketeers game using artificial intelligence and game theory. Capstone Project. Al Akhawayn University.</p>
 </html>