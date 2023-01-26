guess = [0.3, 0.5];
a = fmincon(@NewMSE, guess, [-1 0; 0 -1], [0 0]);