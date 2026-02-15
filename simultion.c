#include <stdio.h>
#include <math.h>
#include <stdlib.h>

/* 
 * Billiard Simulator (Circular & Semi-Circular)
 * 
 * Simulates a ball bouncing inside a circular or semi-circular table.
 * Assumes perfect elastic collisions and no friction.
 */

typedef struct ball { 
    double x, y, angle;
} ball;

/*
 * simulation()
 * Calculates the next bounce position and updates the ball's angle.
 * 
 * ball   -> pointer to our ball struct
 * radius -> table radius
 * mode   -> 0 for Circle, 1 for Semi-Circular (flat bottom at y=0)
 */
void simulation(ball* b, double radius, int mode) {
    double x0 = b->x;
    double y0 = b->y;
    double alpha = b->angle;

    // 1- Solve intersection with the circle boundary
    // We plug the parametric line equations into the circle equation x^2 + y^2 = r^2
    // This gives us a quadratic for 't' (time to collision).
    double a = x0 * cos(alpha) + y0 * sin(alpha);
    double k = x0 * x0 + y0 * y0 - radius * radius; 
    double delta = a * a - k;
    
    if (delta < 0) return; // Ball is somehow outside; ignore.
    
    double t = sqrt(delta) - a; // The time 't' until we hit the wall

    // 2- Find the potential new coordinates on the circle
    double new_x = x0 + cos(alpha) * t;
    double new_y = y0 + sin(alpha) * t;

    // 3- Handle the collision
    // If we're in Semi-Circle mode AND we went below y=0, we hit the flat wall instead.
    if (mode == 1 && new_y < 0) {
        // Calculate intersection with the flat line y=0
        double t_flat = -y0 / sin(alpha); 
        
        b->x = x0 + cos(alpha) * t_flat;
        b->y = 0.0;        // Snap to the flat surface
        b->angle = -alpha; // Simple reflection: just flip the vertical angle
    } 
    else {
        // Normal collision with the curved wall
        b->x = new_x;
        b->y = new_y;
        
        // Calculate reflection using the normal angle (phi)
        // Formula: new_angle = 2*phi - old_angle + PI
        double phi = atan2(new_y, new_x);
        b->angle = 2 * phi - alpha + M_PI;
    }
}

// Helper: Check if file exists before running it
int file_exists(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file) {
        fclose(file);
        return 1;
    }
    return 0;
}

int main() {
    double r = 7.5;  // Table radius
    int n = 30;      // Iterations
    ball a;
    int mode;

    // Setup
    printf("╔════════════════════════════════════════╗\n");
    printf("║  BILLIARD TRAJECTORY SIMULATOR         ║\n");
    printf("╚════════════════════════════════════════╝\n\n");
    printf("Select Simulation Mode:\n");
    printf("  1. Circular billiard (full circle)\n");
    printf("  2. Semi-circular billiard (flat bottom)\n");
    printf("Choice: ");
    
    if (scanf("%d", &mode) != 1) return 1; // Basic input check
    
    if (mode != 1 && mode != 2) {
        printf("Invalid choice.\n");
        return 1;
    }
    
    // Map input (1/2) to logic (0/1)
    int sim_type = (mode == 2) ? 1 : 0; 

        // --- Get Valid Start Position ---
    do {
        printf("\nEnter initial X coordinate: ");
        scanf("%lf", &a.x);
        
        printf("Enter initial Y coordinate: ");
        scanf("%lf", &a.y);
        
        // Check 1: Is it inside the circle? (x^2 + y^2 < r^2)
        double dist_sq = a.x*a.x + a.y*a.y;
        
        if (dist_sq >= r*r) {
            printf("Error: Position (%.2f, %.2f) is OUTSIDE the billiard table (r=%.1f).\n", a.x, a.y, r);
            printf("Please try again.\n");
            continue; // Skip the rest and ask again
        }

        // Check 2: If Semi-Circle mode, y must not be negative
        if (sim_type == 1 && a.y < 0) {
            printf("Error: In Semi-Circular mode, Y cannot be negative.\n");
            printf("Please try again.\n");
            continue;
        }
        
        // If we got here, the input is valid!
        break; 

    } while (1); // Infinite loop until we hit 'break'
    
    printf("Enter initial angle (radians): ");
    scanf("%lf", &a.angle);


    // Run Simulation
    FILE *f = fopen("simulation_data.txt", "w");
    if (!f) { printf("Error opening file.\n"); return 1; }
    
    fprintf(f, "%lf %lf\n", a.x, a.y); // Log start position
    printf("\nStart: %.2f, %.2f\n", a.x, a.y);
    
    for (int i = 1; i <= n; ++i) {
        simulation(&a, r, sim_type);
        
        fprintf(f, "%lf %lf\n", a.x, a.y); // Save to file
        printf("Bounce %d: x=%.2f, y=%.2f\n", i, a.x, a.y);
    }
    
    fclose(f);
    printf("\nDone. Data saved to simulation_data.txt\n");

    // Auto-Launch visualization
    if (file_exists("plot_billiard.py")) {
        printf("Launching visualization...\n");
        system("python3 plot_billiard.py"); // Runs the python script
    } else {
        printf("Note: 'plot_billiard.py' not found. Skipping visualization.\n");
    }
    
    return 0;
}

