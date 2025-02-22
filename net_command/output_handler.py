def print_output(results):
    for task_name, outputs in results.items():
        print("=" * 10 + f" {task_name} " + "=" * 10)
        for output_set in outputs:
            if isinstance(output_set, list):
                for output in output_set:
                    if isinstance(output, str) and "--------------------" in output:
                        print(output.replace("--------------------", "").strip())
                    else:
                        print(output)
                    print("-" * 20)
            else:
                print(output_set)
                print("-" * 20)
    print("=" * 20)
