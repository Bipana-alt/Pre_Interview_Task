
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 4096 /* grid dimension (including boundary) */
#define K 100  /* number of Jacobi iterations */

/* Wall-clock time in seconds */
static double now(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main(void) {
    /* Allocate two N x N grids on the heap */
    double *u = calloc(N * N, sizeof(double));
    double *u_new = calloc(N * N, sizeof(double));
    if (!u || !u_new) { perror("calloc"); return 1; }

    /* Initialize: hot-spot in the top-left quadrant */
    for (int i = 0; i < N/4; i++)
        for (int j = 0; j < N/4; j++)
            u[i*N + j] = 1.0;

    double t0 = now();

    /* ---- kernel: DO NOT change the stencil formula ---- */
    for (int t = 0; t < K; t++) {
        for (int i = 1; i < N-1; i++)
            for (int j = 1; j < N-1; j++)
                u_new[i*N+j] = 0.25 * (u[(i-1)*N+j] + u[(i+1)*N+j]
                                    + u[i*N+j-1] + u[i*N+j+1]);
        /* swap pointers */
        double *tmp = u; u = u_new; u_new = tmp;
    }
    /* ---- end kernel ---- */

    double elapsed = now() - t0;

    /* Quick sanity print: grid checksum */
    double checksum = 0.0;
    for (int i = 0; i < N*N; i++) checksum += u[i];
    printf("checksum = %.10f\n", checksum);
    printf("time = %.4f s\n", elapsed);

    /* Authoritative correctness artifact: dump final grid to disk for
     * element-wise comparison against other variants. */
    FILE *fp = fopen("output.bin", "wb");
    if (!fp) { perror("fopen"); return 1; }
    fwrite(u, sizeof(double), (size_t)N*N, fp);
    fclose(fp);

    free(u); free(u_new);
    return 0;
}
