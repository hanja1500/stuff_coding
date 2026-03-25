#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_RANGE 100.0
#define STEP 0.001

// 그래프 설정을 위한 상수
#define GRAPH_WIDTH 70
#define GRAPH_HEIGHT 20
#define X_MIN -10.0
#define X_MAX 10.0
#define Y_MIN -50.0
#define Y_MAX 50.0

// 1. 다항식 출력 함수
void print_poly(int *coef, int degree, const char* prefix) {
    printf("%s", prefix);
    int is_zero = 1;

    for (int i = 0; i <= degree; i++) {
        if (coef[i] == 0) continue;
        is_zero = 0;
        int power = degree - i;

        if (coef[i] > 0 && i > 0) printf("+ ");
        else if (coef[i] < 0 && i > 0) printf("- ");
        else if (coef[i] < 0 && i == 0) printf("-");

        int abs_c = abs(coef[i]);

        if (abs_c != 1 || power == 0) printf("%d", abs_c);

        if (power > 1) printf("x^%d ", power);
        else if (power == 1) printf("x ");
        else printf(" ");
    }

    if (is_zero) printf("0");
    printf("\n");
}

// 2. 도함수 계수 계산 함수
void calc_derivative(int *in_coef, int in_deg, int *out_coef, int *out_deg) {
    if (in_deg == 0) {
        out_coef[0] = 0;
        *out_deg = 0;
        return;
    }
    *out_deg = in_deg - 1;
    for (int i = 0; i <= *out_deg; i++) {
        out_coef[i] = in_coef[i] * (in_deg - i);
    }
}

// 3. 호너의 방법을 이용한 y값 계산 함수
double evaluate_poly(int *coef, int degree, double x) {
    double result = coef[0];
    for (int i = 1; i <= degree; i++) {
        result = result * x + coef[i];
    }
    return result;
}

// 4. 근 찾기 함수
void find_roots(int *coef, int degree, const char* name) {
    printf("Roots of [%s] (range %.1f ~ %.1f):\n", name, -MAX_RANGE, MAX_RANGE);
    int root_found = 0;

    double prev_y = evaluate_poly(coef, degree, 0.0);

    for (double x = -MAX_RANGE; x <= MAX_RANGE; x += STEP) {
        double y = evaluate_poly(coef, degree, x);

        if ((prev_y > 0 && y <= 0) || (prev_y < 0 && y >= 0)) {
            printf(" -> around x = %.3f\n", x - (STEP / 2.0));
            root_found = 1;
        }
        prev_y = y;
    }

    if (!root_found) printf(" -> No roots found.\n");
    printf("\n");
}

// --- 새롭게 추가된 그래프 매핑 도우미 함수 ---
int map_x(double x) {
    return (int)((x - X_MIN) / (X_MAX - X_MIN) * (GRAPH_WIDTH - 1));
}

int map_y(double y) {
    // 터미널은 위에서 아래로 줄이 넘어가므로, y축을 뒤집어 줍니다.
    return GRAPH_HEIGHT - 1 - (int)((y - Y_MIN) / (Y_MAX - Y_MIN) * (GRAPH_HEIGHT - 1));
}

// 5. 터미널 기반 DOS 스타일 그래프 그리기 함수
void plot_graph(int *ori_coef, int ori_deg, int *d1_coef, int d1_deg, int *d2_coef, int d2_deg) {
    char grid[GRAPH_HEIGHT][GRAPH_WIDTH];

    // 1) 그리드 초기화 (빈 칸으로 채우기)
    for (int r = 0; r < GRAPH_HEIGHT; r++) {
        for (int c = 0; c < GRAPH_WIDTH; c++) {
            grid[r][c] = ' ';
        }
    }

    // 2) x축, y축 그리기
    int origin_c = map_x(0.0);
    int origin_r = map_y(0.0);

    for (int r = 0; r < GRAPH_HEIGHT; r++) {
        if (origin_c >= 0 && origin_c < GRAPH_WIDTH) grid[r][origin_c] = '|';
    }
    for (int c = 0; c < GRAPH_WIDTH; c++) {
        if (origin_r >= 0 && origin_r < GRAPH_HEIGHT) grid[origin_r][c] = '-';
    }
    if (origin_r >= 0 && origin_r < GRAPH_HEIGHT && origin_c >= 0 && origin_c < GRAPH_WIDTH) {
        grid[origin_r][origin_c] = '+'; // 원점
    }

    // 3) 각 x 좌표마다 y값을 계산하여 그래프에 찍기
    for (int c = 0; c < GRAPH_WIDTH; c++) {
        // 현재 열(column)에 해당하는 실제 x값 계산
        double x = X_MIN + (double)c / (GRAPH_WIDTH - 1) * (X_MAX - X_MIN);

        // 원본 함수 점 찍기 (*)
        double y_ori = evaluate_poly(ori_coef, ori_deg, x);
        int r_ori = map_y(y_ori);
        if (r_ori >= 0 && r_ori < GRAPH_HEIGHT) grid[r_ori][c] = '*';
    }

    // 4) 터미널에 출력
    printf("\n--- Graph (X: %.1f to %.1f, Y: %.1f to %.1f) ---\n", X_MIN, X_MAX, Y_MIN, Y_MAX);
    for (int r = 0; r < GRAPH_HEIGHT; r++) {
        for (int c = 0; c < GRAPH_WIDTH; c++) {
            putchar(grid[r][c]);
        }
        putchar('\n');
    }
    printf("------------------------------------------------------\n");
}

int main() {
    int degree = 0;

    printf("Highest degree of the polynomial (e.g., 3 for cubic) : ");
    if (scanf("%d", &degree) != 1) return 1;

    int input_size = degree + 1;
    int ori_coef[100] = {0, };
    int der1_coef[100] = {0, };
    int der2_coef[100] = {0, };
    int der1_deg, der2_deg;

    for (int i = 0; i < input_size; i++) {
        printf("Coefficient of x^%d : ", degree - i);
        if (scanf("%d", &ori_coef[i]) != 1) return 1;
    }

    printf("\n==================================\n");

    calc_derivative(ori_coef, degree, der1_coef, &der1_deg);
    calc_derivative(der1_coef, der1_deg, der2_coef, &der2_deg);

    print_poly(ori_coef, degree, "Original Function : ");
    print_poly(der1_coef, der1_deg, "1st Derivative    : ");
    print_poly(der2_coef, der2_deg, "2nd Derivative    : ");

    printf("==================================\n\n");

    find_roots(ori_coef, degree, "Original Function");
    find_roots(der1_coef, der1_deg, "1st Derivative");
    find_roots(der2_coef, der2_deg, "2nd Derivative");

    // 방금 계산한 세 다항식을 터미널 그래프로 출력합니다!
    plot_graph(ori_coef, degree, der1_coef, der1_deg, der2_coef, der2_deg);

    return 0;
}