def print_output(results):
    success_count = 0
    failure_count = 0

    for task_name, outputs in results.items():
        print("=" * 10 + f" {task_name} " + "=" * 10)
        for output_set in outputs:
            if isinstance(output_set, list):
                for output in output_set:
                    if isinstance(output, str) and (
                        "Error:" in output or "Exception" in output
                    ):
                        failure_count += 1
                        print(output)
                    elif isinstance(output, str) and "--------------------" in output:
                        print(output.replace("--------------------", "").strip())
                        success_count += 1
                    else:
                        print(output)
                        success_count += 1
                    print("-" * 20)
            else:
                if isinstance(output_set, str) and (
                    "Error:" in output_set or "Exception" in output_set
                ):
                    failure_count += 1
                    print(output_set)
                else:
                    print(output_set)
                    success_count += 1
                print("-" * 20)
    print("=" * 20)
    print(f"Summary: {success_count} tasks succeeded, {failure_count} tasks failed")
